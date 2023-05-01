#!/bin/bash
npx caliper launch manager \
  --caliper-workspace ./ \
  --caliper-networkconfig networks/networkConfig.yaml \
  --caliper-benchconfig benchmarks/myAssetBenchmark.yaml \
  --caliper-flow-only-test \
  --caliper-fabric-gateway-enabled \
  --log-level debug