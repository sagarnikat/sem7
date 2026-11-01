'use strict';

/*
 * QUESTION 6 (BT): Business network on Hyperledger Fabric.
 *
 * This chaincode keeps a simple business registry on a permissioned Fabric
 * channel. Each business is stored as JSON under the key BUSINESS_<id>.
 *
 *   createBusiness  add a new record (fails if the id already exists)
 *   readBusiness    return one record
 *   updateBusiness  replace the fields of an existing record
 *   deleteBusiness  remove a record
 *   businessExists  check whether an id is present
 *   getAllBusinesses return every record, used by the dashboard/query step
 *
 * Fabric runs this code inside a Docker peer. The peer reaches consensus
 * through an ordering service; there is no mining and no gas fee. Every
 * create/update/delete is written to the channel ledger and emits an event,
 * so all participating organisations see the same history.
 *
 * The contract API is from fabric-contract-api. ctx.stub.getState() reads
 * the world state, putState() writes it and deleteState() removes it.
 */

const { Contract } = require('fabric-contract-api');

const PREFIX = 'BUSINESS_';
const KEY_END = 'BUSINESS_~';

class BusinessNetworkContract extends Contract {

    keyFor(id) {
        return PREFIX + id;
    }

    async businessExists(ctx, id) {
        const data = await ctx.stub.getState(this.keyFor(id));
        return data && data.length > 0;
    }

    async createBusiness(ctx, id, name, owner, category, active) {
        if (!id || !name || !owner || !category) {
            throw new Error('id, name, owner and category are required');
        }
        if (await this.businessExists(ctx, id)) {
            throw new Error(`business ${id} already exists`);
        }

        const record = {
            id,
            name,
            owner,
            category,
            active: String(active).toLowerCase() === 'true',
            updatedBy: ctx.clientIdentity.getID(),
            updatedAt: new Date().toISOString(),
        };

        await ctx.stub.putState(this.keyFor(id),
            Buffer.from(JSON.stringify(record)));
        ctx.stub.setEvent('BusinessCreated',
            Buffer.from(JSON.stringify(record)));
        return JSON.stringify(record);
    }

    async readBusiness(ctx, id) {
        const data = await ctx.stub.getState(this.keyFor(id));
        if (!data || data.length === 0) {
            throw new Error(`business ${id} does not exist`);
        }
        return data.toString();
    }

    async updateBusiness(ctx, id, name, owner, category, active) {
        if (!(await this.businessExists(ctx, id))) {
            throw new Error(`business ${id} does not exist`);
        }

        const record = {
            id,
            name,
            owner,
            category,
            active: String(active).toLowerCase() === 'true',
            updatedBy: ctx.clientIdentity.getID(),
            updatedAt: new Date().toISOString(),
        };

        await ctx.stub.putState(this.keyFor(id),
            Buffer.from(JSON.stringify(record)));
        ctx.stub.setEvent('BusinessUpdated',
            Buffer.from(JSON.stringify(record)));
        return JSON.stringify(record);
    }

    async deleteBusiness(ctx, id) {
        if (!(await this.businessExists(ctx, id))) {
            throw new Error(`business ${id} does not exist`);
        }

        await ctx.stub.deleteState(this.keyFor(id));
        ctx.stub.setEvent('BusinessDeleted', Buffer.from(id));
        return id;
    }

    async getAllBusinesses(ctx) {
        const iterator = await ctx.stub.getStateByRange(PREFIX, KEY_END);
        const records = [];
        let result = await iterator.next();

        while (!result.done) {
            const value = result.value;
            if (value && value.value.length > 0) {
                records.push(JSON.parse(value.value.toString()));
            }
            result = await iterator.next();
        }

        await iterator.close();
        return JSON.stringify(records);
    }
}

module.exports = BusinessNetworkContract;

// END OF CHAINCODE
// The registry is deliberately small: one asset type, one key prefix and
// six functions. Fabric stores the history of every key, so the peer CLI or
// a block explorer can show all earlier versions even after an update.
