package com.example.diminishedreality

import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import java.io.IOException
import java.util.concurrent.TimeUnit

//Author: Vincent Hald

object DiminishingAPI {
    private val JSON = MediaType.parse("application/json; charset=utf-8")

    //Configure timeouts for long running image processing
    val client = OkHttpClient.Builder()
        .readTimeout(60, TimeUnit.SECONDS)
        .connectTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    //Send post request to specified url containing json as body
    //Don't send full body on first try for optimization, because backend always sends status code
    //308 "permanent redirect" on first request
    @Throws(IOException::class)
    fun post(url: String?, json: String?, isRedirect: Boolean?): String? {
        var bodyString = ""

        //only fill body after redirect
        if (isRedirect == true) {
            bodyString = json!!
        }
        val body = RequestBody.create(JSON, bodyString)

        //build simple HTTP request using URL and body contents
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()
        client.newCall(request).execute().use { response ->
            return if (response.code() == 308) {
                //when status code 308 is returned, retrieve the new url from Location header field
                //and call post function again
                val location = response.header("Location")
                post(location, json, true)
            } else {
                //response does not indicate redirect -> return either valid result or error message
                response.body()!!.string()
            }
        }
    }
}
