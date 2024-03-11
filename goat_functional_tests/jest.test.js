const axios = require('axios');

// Assuming axios is set up for making HTTP requests

describe('GOAT Application Functional Tests', () => {
    let jamesToken, larsToken, jamesUid, larsUid;
    const baseUrl = "http://44.202.3.35:6000";

    // Helper function to login users
    async function loginUser(userName, password) {
        const response = await axios.post(`${baseUrl}/login`, { userName, password });
        return response;
    }

    // Helper function to get account info
    async function getAccount(token) {
        const response = await axios.get(`${baseUrl}/account`, { headers: { Authorization: `Bearer ${token}` } });
        return response;
    }

    // Helper function to get transactions
    async function getTransactions(token, uid, limit) {
        const response = await axios.get(`${baseUrl}/transactions`, {
            params: { limit, userId: uid },
            headers: { Authorization: `Bearer ${token}` }
        });
        return response;
    }

    beforeAll(async () => {
        // Login both users before all tests
        const jamesLoginResponse = await loginUser("James", "ILoveGuitars");
        jamesToken = jamesLoginResponse.data.token;

        const larsLoginResponse = await loginUser("Lars", "ILoveDrums");
        larsToken = larsLoginResponse.data.token;
    });

    test('James can login and get user info', async () => {
        const accountResponse = await getAccount(jamesToken);
        expect(accountResponse.status).toBe(200);
        jamesUid = accountResponse.data.userId;
    });

    test('James can get transactions', async () => {
        const transactionsResponse = await getTransactions(jamesToken, jamesUid, 5);
        expect(transactionsResponse.status).toBe(200);
        expect(transactionsResponse.data.length).toBe(5);

        const moreTransactionsResponse = await getTransactions(jamesToken, jamesUid, 10);
        expect(moreTransactionsResponse.status).toBe(200);
        expect(moreTransactionsResponse.data.length).toBe(10);
    });

    test('Lars can login and get user info', async () => {
        const accountResponse = await getAccount(larsToken);
        expect(accountResponse.status).toBe(200);
        larsUid = accountResponse.data.userId;
    });

    test('Lars can get transactions', async () => {
        const transactionsResponse = await getTransactions(larsToken, larsUid, 5);
        expect(transactionsResponse.status).toBe(200);
        expect(transactionsResponse.data.length).toBe(5);
    });

    // Add any additional tests following the patterns above
});
