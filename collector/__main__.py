"""
Ponto de entrada CLI do coletor AWS-Horus.

Uso:
  python -m collector --external-id SEU_EXTERNAL_ID
  python -m collector --external-id SEU_EXTERNAL_ID --account 123456789012
"""
import argparse
import json
import sys
from collector.collector import HorusCollector
from collector.extractors.dedicated import LambdaExtractor
from collector.extractors.network import SecurityGroupExtractor, VPCExtractor
from collector.extractors.compute_data import EC2Extractor, RDSExtractor, S3Extractor
from collector.extractors.priority_services import EKSExtractor, CloudFrontExtractor, APIGatewayExtractor, OpenSearchExtractor
from collector.extractors.remaining_services import MWAAExtractor, GlueExtractor, DMSExtractor, MQExtractor, WAFExtractor, EFSExtractor

def main():
    parser = argparse.ArgumentParser(description="AWS-Horus Collector")
    parser.add_argument("--external-id", required=True, help="ExternalId da role AtlasReadOnly")
    parser.add_argument("--account", help="Filtrar para uma conta específica (opcional)")
    parser.add_argument("--output", default="-", help="Arquivo de saída JSON (ou - para stdout)")
    args = parser.parse_args()

    collector = HorusCollector(external_id=args.external_id)

    for ext in [
        SecurityGroupExtractor(), VPCExtractor(),
        EC2Extractor(), RDSExtractor(), S3Extractor(), LambdaExtractor(),
        EKSExtractor(), CloudFrontExtractor(), APIGatewayExtractor(), OpenSearchExtractor(),
        MWAAExtractor(), GlueExtractor(), DMSExtractor(), MQExtractor(), WAFExtractor(), EFSExtractor(),
    ]:
        collector.register_extractor(ext)

    print("Iniciando full scan...", file=sys.stderr)
    result = collector.full_scan()

    if args.output == "-":
        print(json.dumps(result, indent=2, default=str))
    else:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Resultado salvo em {args.output}", file=sys.stderr)

if __name__ == "__main__":
    main()
