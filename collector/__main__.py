"""
Ponto de entrada CLI do coletor AWS-Horus.
"""
import argparse
import json
import sys
from collector.collector import HorusCollector
from collector.extractors.network import SecurityGroupExtractor, VPCExtractor
from collector.extractors.compute_data import EC2Extractor, RDSExtractor, S3Extractor
from collector.extractors.dedicated import LambdaExtractor
from collector.extractors.integration import ELBExtractor, CloudFrontExtractor, APIGatewayExtractor, EKSExtractor
from collector.extractors.priority_services import OpenSearchExtractor
from collector.extractors.remaining_services import MWAAExtractor, GlueExtractor, DMSExtractor, WAFExtractor, EFSExtractor
from collector.extractors.remaining_complete import Route53Extractor, ACMExtractor, ECRExtractor, BackupExtractor, ConfigExtractor, MQExtractor

def main():
    parser = argparse.ArgumentParser(description="AWS-Horus Collector")
    parser.add_argument("--external-id", required=True)
    parser.add_argument("--output", default="-")
    args = parser.parse_args()

    collector = HorusCollector(external_id=args.external_id)

    for ext in [
        SecurityGroupExtractor(), VPCExtractor(),
        EC2Extractor(), RDSExtractor(), S3Extractor(), LambdaExtractor(),
        ELBExtractor(), CloudFrontExtractor(), APIGatewayExtractor(), EKSExtractor(),
        OpenSearchExtractor(), MWAAExtractor(), GlueExtractor(), DMSExtractor(),
        WAFExtractor(), EFSExtractor(),
        Route53Extractor(), ACMExtractor(), ECRExtractor(), BackupExtractor(),
        ConfigExtractor(), MQExtractor(),
    ]:
        collector.register_extractor(ext)

    print("Iniciando full scan...", file=sys.stderr)
    result = collector.full_scan()

    if args.output == "-":
        print(json.dumps(result, indent=2, default=str))
    else:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, default=str)

if __name__ == "__main__":
    main()
