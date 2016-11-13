package com.solidarity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.http.HttpMethodName;
import com.amazonaws.mobile.AWSMobileClient;
import com.amazonaws.mobile.api.CloudLogicAPI;
import com.amazonaws.mobile.api.idh8tj4utro7.SwaggerAPIClient;
import com.amazonaws.mobile.api.idh8tj4utro7.model.Empty;
import com.amazonaws.mobile.user.IdentityManager;
import com.amazonaws.mobileconnectors.apigateway.ApiClientFactory;
import com.amazonaws.mobileconnectors.apigateway.ApiRequest;
import com.amazonaws.mobileconnectors.apigateway.ApiResponse;
import com.amazonaws.util.StringUtils;


import java.util.HashMap;
import java.util.Map;

/**
 * Created by Derek on 11/12/2016.
 */

public class CreateGroupActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_group);
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    public void submit(View view) {
        invokeAPI();
    }

    public void invokeAPI() {

        final String LOG_TAG = CreateGroupActivity.class.getSimpleName();
        // Set your request method, path, query string parameters, and request body
        final String method = "POST";
        final String path = "/items";
        final String body = "{\"someParameter\":\"someValue\"}";
        final Map<String, String> queryStringParameters = new HashMap<String, String>();
        final Map<String, String> headers = new HashMap<String, String>();

        final byte[] content = body.getBytes(StringUtils.UTF8);
        // Create an instance of your custom SDK client
        final AWSMobileClient mobileClient = AWSMobileClient.defaultMobileClient();
        final CloudLogicAPI client = mobileClient.createAPIClient(SwaggerAPIClient.class);

        // Construct the request
        final ApiRequest request =
                new ApiRequest(client.getClass().getSimpleName())
                        .withPath(path)
                        .withHttpMethod(HttpMethodName.valueOf(method))
                        .withHeaders(headers)
                        .addHeader("Content-Type", "application/json")
                        .addHeader("Content-Length", String.valueOf(content.length))
                        .withParameters(queryStringParameters)
                        .withBody(content);

        // Make network call on background thread
        new Thread(new Runnable() {

            @Override
            public void run() {
                try {

                    // Invoke the API
                    final ApiResponse response = client.execute(request);

                    final int statusCode = response.getStatusCode();
                    final String statusMessage = response.getStatusText();

                    Log.d(LOG_TAG, "Response Status: " + statusCode + " " + statusMessage);

                    // TODO: Add your custom handling for server response status codes (e.g., 403 Forbidden)

                } catch (final AmazonClientException exception) {
                    Log.e(LOG_TAG, exception.getMessage(), exception);

                    // TODO: Put your exception handling code here (e.g., network error)
                }
            }
        }).start();
    }
}
