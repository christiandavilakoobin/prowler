from lib.check.models import Check, Check_Report
from providers.aws.services.ec2.ec2_client import ec2_client
from providers.aws.services.ec2.lib.network_acls import check_network_acl


class ec2_networkacl_allow_ingress_any_port(Check):
    def execute(self):
        findings = []
        tcp_protocol = "-1"
        check_port = 0
        for network_acl in ec2_client.network_acls:
            report = Check_Report(self.metadata())
            report.region = network_acl.region
            report.resource_id = network_acl.id
            # If some entry allows it, that ACL is not securely configured
            if not check_network_acl(network_acl.entries, tcp_protocol, check_port):
                report.status = "PASS"
                report.status_extended = f"Network ACL {network_acl.id} has not every port open to the Internet."
            else:
                report.status = "FAIL"
                report.status_extended = (
                    f"Network ACL {network_acl.id} has every port open to the Internet."
                )
            findings.append(report)

        return findings