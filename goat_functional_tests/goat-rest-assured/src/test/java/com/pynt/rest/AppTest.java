package com.pynt.rest;

import org.junit.Test;
import org.junit.runners.MethodSorters;
import org.json.JSONObject;
import org.json.JSONException;
import org.junit.FixMethodOrder;

import static io.restassured.RestAssured.* ;
import static io.restassured.matcher.RestAssuredMatchers.* ;
import static org.hamcrest.Matchers.* ;

/**
 * Unit test for simple App.
 */
@FixMethodOrder( MethodSorters.NAME_ASCENDING )
public class AppTest 
{

    static String jamesToken; 
    static String larsToken; 
    static String jamesUid; 
    static String larsUid;

    /**
     * Rigorous Test :-)
     */
    @Test
    public void step1_testJamesCanLogin()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;

        try 
        {
            JSONObject body = new JSONObject()
                                  .put("userName", "James")
                                  .put("password", "ILoveGuitars");

            jamesToken = "Bearer " + 
            given()
                .contentType("application/json")
                .body(body.toString())
            .when()
                .post("/login")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().jsonPath().getString("token");

            System.out.println(jamesToken);
        } catch (JSONException e) {
            System.out.println(e);
        }

    }
    
    @Test
    public void step2_testGetJamesAccount()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;
        System.out.println("Will use james token " + jamesToken);
            jamesUid = 
            given()
                .header("Authorization", jamesToken)
            .when()
                .get("/account")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().jsonPath().getString("userId");

            System.out.println(jamesUid);

    }

    @Test
    public void step3_testGetJamesTransactions()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;

            String resp =  
            given()
                .header("Authorization", jamesToken)
                .queryParam("userId", jamesUid)
                .queryParam("limit", 5)
            .when()
                .get("/transactions")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().asString();
            
            System.out.println(resp);
    }

    @Test
    public void step4_testGetMoreOfJamesTransactions()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;

            String resp =  
            given()
                .header("Authorization", jamesToken)
                .queryParam("userId", jamesUid)
                .queryParam("limit", 10)
            .when()
                .get("/transactions")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().asString();
            
            System.out.println(resp);
    }

        @Test
    public void step5_testLarsCanLogin()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;

        try 
        {
            JSONObject body = new JSONObject()
                                  .put("userName", "Lars")
                                  .put("password", "ILoveDrums");

            larsToken = "Bearer " + 
            given()
                .contentType("application/json")
                .body(body.toString())
            .when()
                .post("/login")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().jsonPath().getString("token");

            System.out.println(larsToken);
        } catch (JSONException e) {
            System.out.println(e);
        }
    }
    

    @Test
    public void step6_testGetLarsAccount()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;

            larsUid = 
            given()
                .header("Authorization", larsToken)
            .when()
                .get("/account")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().jsonPath().getString("userId");

            System.out.println(larsUid);

    }

    @Test
    public void step7_testGetLarsTransactions()
    {
        baseURI = "http://44.202.3.35";
        port = 6000;

            String resp =  
            given()
                .header("Authorization", larsToken)
                .queryParam("userId", larsUid)
                .queryParam("limit", 5)
            .when()
                .get("/transactions")
            .then()
                .statusCode(200)
                .extract()
                .response().getBody().asString();
            
            System.out.println(resp);
    }
}
