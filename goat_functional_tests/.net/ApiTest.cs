#nullable enable
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;
using Xunit;
using System.Net.Http.Json;

public class ApiTest : IClassFixture<ApiTest.ApiState>
{
    private readonly HttpClient _client;
    private readonly ApiState _state;
    private const string BaseUrl = "http://44.202.3.35:6000";

    public class ApiState
    {
        public string? JamesToken { get; set; }
        public string? LarsToken { get; set; }
        public string? JamesUid { get; set; }
        public string? LarsUid { get; set; }
    }

    public ApiTest(ApiState state)
    {
        _client = new HttpClient();
        _state = state;
    }

    private async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, string? token = null)
    {
        if (!string.IsNullOrEmpty(token))
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        
        return await _client.SendAsync(request);
    }

    private async Task<HttpResponseMessage> Login(string userName, string password)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, $"{BaseUrl}/login")
        {
            Content = JsonContent.Create(new { userName, password })
        };
        return await SendAsync(request);
    }

    private async Task<HttpResponseMessage> GetAccount(string token)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, $"{BaseUrl}/account");
        return await SendAsync(request, token);
    }

    private async Task<HttpResponseMessage> GetTransactions(string token, string uid, int limit)
    {
        var url = $"{BaseUrl}/transactions?limit={limit}&userId={uid}";
        var request = new HttpRequestMessage(HttpMethod.Get, url);
        return await SendAsync(request, token);
    }

    [Fact]
    public async Task James_Can_Login()
    {
        var response = await Login("James", "ILoveGuitars");
        Assert.True(response.IsSuccessStatusCode);

        var json = await response.Content.ReadAsStringAsync();
        _state.JamesToken = JsonDocument.Parse(json).RootElement.GetProperty("token").GetString();
    }

    [Fact]
    public async Task Get_James_User_Info()
    {
        if (string.IsNullOrEmpty(_state.JamesToken))
        {
            var loginResp = await Login("James", "ILoveGuitars");
            var loginJson = await loginResp.Content.ReadAsStringAsync();
            _state.JamesToken = JsonDocument.Parse(loginJson).RootElement.GetProperty("token").GetString();
        }

        var response = await GetAccount(_state.JamesToken!);
        Assert.True(response.IsSuccessStatusCode);

        var json = await response.Content.ReadAsStringAsync();
        _state.JamesUid = JsonDocument.Parse(json).RootElement.GetProperty("userId").GetString();
    }

    [Fact]
    public async Task Get_James_User_Info_From_GraphQL()
    {
        if (string.IsNullOrEmpty(_state.JamesToken) || string.IsNullOrEmpty(_state.JamesUid))
        {
            await Get_James_User_Info();
        }

        var query = new { query = "query { me { userId } }" };
        var request = new HttpRequestMessage(HttpMethod.Post, $"{BaseUrl}/graphql")
        {
            Content = JsonContent.Create(query)
        };
        var response = await SendAsync(request, _state.JamesToken);

        Assert.True(response.IsSuccessStatusCode);

        var json = await response.Content.ReadAsStringAsync();
        var root = JsonDocument.Parse(json).RootElement;
        var userId = root.GetProperty("data").GetProperty("me").GetProperty("userId").GetString();

        Assert.Equal(_state.JamesUid, userId);
    }

    [Fact]
    public async Task Get_James_Transactions()
    {
        if (string.IsNullOrEmpty(_state.JamesToken) || string.IsNullOrEmpty(_state.JamesUid))
        {
            await Get_James_User_Info();
        }

        var resp5 = await GetTransactions(_state.JamesToken!, _state.JamesUid!, 5);
        Assert.True(resp5.IsSuccessStatusCode);
        var json5 = JsonDocument.Parse(await resp5.Content.ReadAsStringAsync());
        Assert.Equal(5, json5.RootElement.GetArrayLength());

        var resp10 = await GetTransactions(_state.JamesToken!, _state.JamesUid!, 10);
        Assert.True(resp10.IsSuccessStatusCode);
        var json10 = JsonDocument.Parse(await resp10.Content.ReadAsStringAsync());
        Assert.Equal(10, json10.RootElement.GetArrayLength());
    }

    [Fact]
    public async Task Lars_Can_Login()
    {
        var response = await Login("Lars", "ILoveDrums");
        Assert.True(response.IsSuccessStatusCode);

        var json = await response.Content.ReadAsStringAsync();
        _state.LarsToken = JsonDocument.Parse(json).RootElement.GetProperty("token").GetString();
    }

    [Fact]
    public async Task Get_Lars_User_Info()
    {
        if (string.IsNullOrEmpty(_state.LarsToken))
        {
            var loginResp = await Login("Lars", "ILoveDrums");
            var loginJson = await loginResp.Content.ReadAsStringAsync();
            _state.LarsToken = JsonDocument.Parse(loginJson).RootElement.GetProperty("token").GetString();
        }

        var response = await GetAccount(_state.LarsToken!);
        Assert.True(response.IsSuccessStatusCode);

        var json = await response.Content.ReadAsStringAsync();
        _state.LarsUid = JsonDocument.Parse(json).RootElement.GetProperty("userId").GetString();
    }

    [Fact]
    public async Task Get_Lars_Transactions()
    {
        if (string.IsNullOrEmpty(_state.LarsToken) || string.IsNullOrEmpty(_state.LarsUid))
        {
            await Get_Lars_User_Info();
        }

        var response = await GetTransactions(_state.LarsToken!, _state.LarsUid!, 5);
        Assert.True(response.IsSuccessStatusCode);
    }
}
