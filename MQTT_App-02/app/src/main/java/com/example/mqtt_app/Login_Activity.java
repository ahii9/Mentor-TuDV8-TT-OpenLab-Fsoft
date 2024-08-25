package com.example.mqtt_app;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class Login_Activity extends AppCompatActivity {
    private EditText usernameInput;
    private EditText passwordInput;
    private Button loginButton;
    private final static String Topic_login = "login";
    private final static String Topic_logincheck = "login/check";

    public static String userApp;
    private MqttManager mqttManager = MqttManager.getInstance(this);

    public String getUserApp() {
        return userApp;
    }

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signin);
        init();
    }
    private void init() {
        usernameInput = findViewById(R.id.username_input);
        passwordInput = findViewById(R.id.password_input);
        loginButton = findViewById(R.id.login_button);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                performLogin();
            }
        });
    }
    private void performLogin() {
        // Get the input from EditText fields
        String username = usernameInput.getText().toString().trim();
        String password = passwordInput.getText().toString().trim();
        // Validate the input
        if (TextUtils.isEmpty(username)) {
            usernameInput.setError("Please enter your username");
            return;
        }

        if (TextUtils.isEmpty(password)) {
            passwordInput.setError("Please enter your password");
            return;
        }
        String pub_msg = username + "/"+ password;
        mqttManager.publish(Topic_login, pub_msg);
        Toast.makeText(this, "publish login ", Toast.LENGTH_SHORT).show();
        mqttManager.subscribe(Topic_logincheck,1);
        mqttManager.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                String msgcheck = new String(message.getPayload());
                if (topic.equals(Topic_logincheck)) {
                    if (msgcheck.equals("success")) {
                        Toast.makeText(Login_Activity.this, "Login success", Toast.LENGTH_SHORT).show();
                        userApp = username;
                        startActivity(new Intent(Login_Activity.this,HomeActivity.class));
                        finish();
                    } else if (msgcheck.equals("incorrect")) {
                        Toast.makeText(Login_Activity.this, "Username or password incorrect", Toast.LENGTH_SHORT).show();
                        passwordInput.getText().clear();
                    } else if (msgcheck.equals("no username")) {
                        Toast.makeText(Login_Activity.this, "Username does not exist", Toast.LENGTH_SHORT).show();
                        passwordInput.getText().clear();
                    }
                }

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}
