from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from nora_evals.schema import FixtureManifest
from nora_evals.runner import EvalRunner

def main():
    parser = argparse.ArgumentParser(prog="nora-evals", description="nora-evals benchmark runner CLI")
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    run_parser = subparsers.add_parser("run", help="Run a synthetic eval fixture")
    run_parser.add_argument("--fixture", required=True, help="Path to JSON fixture file")
    run_parser.add_argument("--out", help="Path to save machine-readable result bundle JSON")
    
    args = parser.parse_args()
    
    if args.cmd == "run":
        fixture_path = Path(args.fixture).resolve()
        if not fixture_path.exists():
            print(f"Error: Fixture file not found: {fixture_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(fixture_path, encoding="utf-8") as f:
            data = json.load(f)
            
        manifest = FixtureManifest.from_dict(data)
        runner = EvalRunner()
        bundle = runner.run_fixture(manifest)
        
        result_json = json.dumps(bundle.to_dict(), indent=2)
        if args.out:
            out_path = Path(args.out).resolve()
            out_path.write_text(result_json + "\n", encoding="utf-8")
            print(f"Result bundle saved to: {out_path}")
        else:
            print(result_json)
            
        sys.exit(0 if bundle.passed_cases == bundle.total_cases else 1)

if __name__ == "__main__":
    main()
