package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"strconv"
	"testing"

	"github.com/stretchr/testify/assert"
)

var (
	jamesToken string
	larsToken  string
	jamesUID   string
	larsUID    string
)

const baseURL = "http://44.202.3.35:6000"

type loginResponse struct {
	Token string `json:"token"`
}

type accountResponse struct {
	UserID string `json:"userId"`
}

func sendRequest(req *http.Request, authorization string) (*http.Response, error) {
	client := &http.Client{}
	if authorization != "" {
		req.Header.Set("Authorization", "Bearer "+authorization)
	}
	return client.Do(req)
}

func login(userName, password string) (*http.Response, error) {
	body := map[string]string{
		"userName": userName,
		"password": password,
	}
	jsonBody, _ := json.Marshal(body)
	req, _ := http.NewRequest("POST", baseURL+"/login", bytes.NewBuffer(jsonBody))
	req.Header.Set("Content-Type", "application/json")
	return sendRequest(req, "")
}

func getAccount(authorization string) (*http.Response, error) {
	req, _ := http.NewRequest("GET", baseURL+"/account", nil)
	return sendRequest(req, authorization)
}

func getTransactions(authorization, uid string, limit int) (*http.Response, error) {
	req, _ := http.NewRequest("GET", baseURL+"/transactions?limit="+strconv.Itoa(limit)+"&userId="+uid, nil)
	return sendRequest(req, authorization)
}

func TestJamesCanLogin(t *testing.T) {
	resp, err := login("James", "ILoveGuitars")
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ := ioutil.ReadAll(resp.Body)
	var loginResp loginResponse
	json.Unmarshal(body, &loginResp)
	jamesToken = loginResp.Token
}

func TestGetJamesUserInfo(t *testing.T) {
	assert.NotNil(t, jamesToken)
	resp, err := getAccount(jamesToken)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ := ioutil.ReadAll(resp.Body)
	var accountResp accountResponse
	json.Unmarshal(body, &accountResp)
	jamesUID = accountResp.UserID
}

func TestGetJamesTransactions(t *testing.T) {
	assert.NotNil(t, jamesToken)
	assert.NotNil(t, jamesUID)

	resp, err := getTransactions(jamesToken, jamesUID, 5)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ := ioutil.ReadAll(resp.Body)
	var transactions []map[string]interface{}
	json.Unmarshal(body, &transactions)
	assert.Len(t, transactions, 5)

	resp, err = getTransactions(jamesToken, jamesUID, 10)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ = ioutil.ReadAll(resp.Body)
	json.Unmarshal(body, &transactions)
	assert.Len(t, transactions, 10)
}

func TestLarsCanLogin(t *testing.T) {
	resp, err := login("Lars", "ILoveDrums")
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ := ioutil.ReadAll(resp.Body)
	var loginResp loginResponse
	json.Unmarshal(body, &loginResp)
	larsToken = loginResp.Token
}

func TestGetLarsUserInfo(t *testing.T) {
	assert.NotNil(t, larsToken)
	resp, err := getAccount(larsToken)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ := ioutil.ReadAll(resp.Body)
	var accountResp accountResponse
	json.Unmarshal(body, &accountResp)
	larsUID = accountResp.UserID
}

func TestGetLarsTransactions(t *testing.T) {
	assert.NotNil(t, larsToken)
	assert.NotNil(t, larsUID)

	resp, err := getTransactions(larsToken, larsUID, 5)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	body, _ := ioutil.ReadAll(resp.Body)
	var transactions []map[string]interface{}
	json.Unmarshal(body, &transactions)
	assert.Len(t, transactions, 5)
}
