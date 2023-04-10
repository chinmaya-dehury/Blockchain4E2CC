Table 1: Test Configuration Table
| Parameter | Value |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Consensus | Solo |
| Network Size | 5 |
| Block Size | 5000 |
| Geographic distribution of nodes | Nodes are docker containers |
| Hardware environment of all peers | 2GZ, 64GB RAM |
| Network model | NA |
| Number of nodes involved in the test transaction | 5 |
| Software component dependencies | NA |
| Test tools and framework | Hyperledger Caliper |
| Transaction rate | 3000 TPS |
| Load | Linear |
| Metrics monitoring | Prometheus |
| Visualization | Grafana |
| Type of data store used | CouchDB |
| Workload | Fixed |

Table 2: Measurements Table

| Metric                 | Formula                                                                 | Definition                                                                                                                                                               |
| ---------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Read Latency           | Time when response received - submit time                               | The time between when the read request is submitted and when the reply is received                                                                                       |
| Read Throughput        | Total read operations / total time in seconds                           | The number of read operations completed in a defined time period, expressed as reads per second (RPS)                                                                    |
| Transaction Latency    | (Confirmation time @ network threshold) - submit time                   | The amount of time taken for a transaction's effect to be usable across the network, measured from the point it is submitted to the point the result is widely available |
| Transaction Throughput | Total committed transactions / total time in seconds @ #committed nodes | The rate at which valid transactions are committed by the blockchain SUT in a defined time period, expressed as transactions per second (TPS) at a network size          |

Table 3: Metrics Table

| Measurements           | Unit           |
| ---------------------- | -------------- |
| Throughput             | # no of trans. |
| Execution Time         | sec            |
| Transaction Latency    | sec            |
| Response Time          | sec            |
| Block Propagation Time | sec            |
| Consensus Time         | sec            |
| Network Latency        | sec            |
