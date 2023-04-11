'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

class MyWorkload extends WorkloadModuleBase {
    constructor() {
        super();
        this.callCounter = 0;
    }

    async initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext) {
        await super.initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext);

        // for (let i=0; i<this.roundArguments.assets; i++) {
        //     console.log("Entering InitWorkModule Phase.....")
        //     //await new Promise(resolve => setTimeout(resolve, 5000));
        //     const assetID = `${this.workerIndex}_${i}`;
        //     console.log(`Worker ${this.workerIndex}: Creating asset ${assetID}`);
        //     let data = {
        //         temperature: '12.34',
        //         timestamp: new Date().toISOString(),
        //         org: 'Tartucitycouncil',
        //         device: 'SensorOne',
        //         arrivalTime: new Date().toISOString(), // time when the data arrived at the fog node
        //       };
        //     const request = {
        //         contractId: this.roundArguments.contractId,
        //         contractFunction: 'put',
        //         //invokerIdentity: 'tartucitycouncilMSP',
        //         contractArguments: [assetID,JSON.stringify(data)],
        //         readOnly: false
        //     };

        //     const result = await this.sutAdapter.sendRequests(request);

        //     let shortID = result.GetID().substring(8);
        //     let executionTime = result.GetTimeFinal() - result.GetTimeCreate();
        //     console.log(`InitModule: TX [${shortID}] took ${executionTime}ms to execute. Result: ${result.GetStatus()}`);
        //     console.log("Leaving InitWorkModule Phase...")
        //     //await new Promise(resolve => setTimeout(resolve, 5000));
        //     this.callCounter++; // increment the counter
        //     console.log(`Init Method called ${this.callCounter} times.`); // print out the updated counter
       // }
    }

    async submitTransaction() {
        const assetID = Math.floor(Math.random()*this.roundArguments.assets);

        let data = {
            temperature: '12.34',
            timestamp: new Date().toISOString(),
            org: 'Tartucitycouncil',
            device: 'SensorOne',
            arrivalTime: new Date().toISOString(), // time when the data arrived at the fog node
          };

        const request = {
            contractId: this.roundArguments.contractId,
            contractFunction: 'put',
            //invokerIdentity: 'User1',
            //contractArguments: [`${this.workerIndex}_${randomId}`],
            contractArguments: [assetID,JSON.stringify(data)],
            readOnly: true
        };

        const result = await this.sutAdapter.sendRequests(request);

        let shortID = result.GetID().substring(8);
        let executionTime = result.GetTimeFinal() - result.GetTimeCreate();
        console.log(`TX [${shortID}] took ${executionTime}ms to execute. Result: ${result.GetStatus()}`);
        this.callCounter++; // increment the counter
        console.log(`Method called ${this.callCounter} times.`); // print out the updated counter
    }
    // async submitTransaction() {
    //     const assetID = Math.floor(Math.random() * this.roundArguments.assets);
    //     //const assetID = `${this.workerIndex}_${i}`;
    //     let contractArguments;
    //     let readOnly;
        
    //     if (this.callCounter % 2 === 0) {
    //       contractArguments = [assetID, JSON.stringify({
    //         temperature: '12.34',
    //         timestamp: new Date().toISOString(),
    //         org: 'Tartucitycouncil',
    //         device: `Sensor${assetID}`,
    //         arrivalTime: new Date().toISOString(),
    //       })];
    //       readOnly = false;
    //     } else {
    //       contractArguments = [assetID, `${this.workerIndex}_${assetID}`];
    //       readOnly = true;
    //     }
        
    //     const myArgs = {
    //       contractId: this.roundArguments.contractId,
    //       contractFunction: 'put',
    //       contractArguments,
    //       readOnly,
    //     };
    
    //     const result = await this.sutAdapter.sendRequests(myArgs);
        
    //     let shortID = result.GetID().substring(8);
    //     let executionTime = result.GetTimeFinal() - result.GetTimeCreate();
    //     console.log(`TX [${shortID}] took ${executionTime}ms to execute. Result: ${result.GetStatus()}`);
    
    //     this.callCounter++;
    //     console.log(`Method called ${this.callCounter} times.`);
    //   }

    // async cleanupWorkloadModule() {
    //     console.log("Calling Delete...")
    //     for (let i=0; i<this.roundArguments.assets; i++) {
    //         const assetID = `${this.workerIndex}_${i}`;
    //         console.log(`Worker ${this.workerIndex}: Deleting asset ${assetID}`);
    //         const request = {
    //             contractId: this.roundArguments.contractId,
    //             contractFunction: 'delete',
    //            // invokerIdentity: 'User1',
    //             contractArguments: [assetID],
    //             readOnly: false
    //         };

    //         await this.sutAdapter.sendRequests(request);
    //     }
    // }
}

function createWorkloadModule() {
    return new MyWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;