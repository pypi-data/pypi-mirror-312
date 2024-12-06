#   -------------------------------------------------------------
#   Platform checks
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Check if a softwareversions is up-to-date
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import re
import requests
import subprocess

from semver import VersionInfo as Version


class HashiCorpSoftwareVersionCheck:
    def __init__(self, software, executable_name=None):
        self.software = software
        if executable_name:
            self.executable_name = executable_name
        else:
            self.executable_name = software

    def perform(self):
        _, last = self.get_last_version()
        current = self.get_current_version()

        last = Version.parse(last)
        current = Version.parse(current)

        if current < last:
            return False, f"can be upgraded from {current} to {last}"

        return True, "up-to-date"

    def get_last_version(self, rc=False):
        url = f"https://releases.hashicorp.com/{self.software}/"
        response = requests.get(url)

        if response.status_code != 200:
            return False, None

        lines = [
            line.strip()
            for line in response.text.split("\n")
            if f"/{self.software}/" in line
        ]

        try:
            for line in lines:
                version = self.extract_published_version(line)

                if "+" in version:
                    continue

                if rc or not is_beta(version):
                    return True, version
        except RuntimeError:
            return False, None

    def extract_published_version(self, expression):
        result = re.findall(r"\/([a-z0-9\-]+)\/(.*?)\/", expression)
        if len(result) != 1:
            raise RuntimeError("Can't extract version")

        software, version = result[0]
        if software != self.software:
            raise RuntimeError("Unexpected software name")

        return version

    def get_current_version(self):
        p = subprocess.run([self.executable_name, "version"], capture_output=True)
        if p.returncode != 0:
            raise RuntimeError("Can't get executable version")

        expression = p.stdout.decode("UTF-8").strip()
        return expression.split()[1][1:]


def is_beta(version):
    return "rc" in version or "beta" in version
