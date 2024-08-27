package com.example.mqtt_app;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class SignUp_Activity extends AppCompatActivity {
    private String Topic_signup = "signup";

    private EditText usernameInput;
    private EditText passwordInput;
    private EditText passwordConfirm;
    private TextView loginButton;
    private Button signupButton;

    private MqttManager mqttManager = MqttManager.getInstance(this);
    private String Topic_signupcheck = "signup/check/"+mqttManager.getMqttClient().getClientId();
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
        init();
    }
    private void init() {
        usernameInput = findViewById(R.id.username_signup);
        passwordInput = findViewById(R.id.password_signup);
        passwordConfirm = findViewById(R.id.password_confirm_signup);
        loginButton = findViewById(R.id.login_txt);
        signupButton = findViewById(R.id.signup_button);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(),Login_Activity.class));
            }
        });
        signupButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                performSignup();
            }
        });
    }
    private void performSignup() {
        String id = mqttManager.getMqttClient().getClientId();
        String username = usernameInput.getText().toString().trim();
        String password = passwordInput.getText().toString().trim();
        String repassword = passwordConfirm.getText().toString().trim();
        // Validate the input
        if (TextUtils.isEmpty(username)) {
            usernameInput.setError("Please enter your username");
            return;
        }

        if (TextUtils.isEmpty(password)) {
            passwordInput.setError("Please enter your password");
            return;
        }
        if (TextUtils.isEmpty(password)) {
            passwordConfirm.setError("Please enter your password");
            return;
        }
        if (!password.equals(repassword)) {
            passwordConfirm.setError("Confirm password is not same as your password");
            return;
        } else {
            String msg = id+"/"+ username+"/"+password;
            mqttManager.publish(Topic_signup,msg);
            mqttManager.subscribe(Topic_signupcheck,1);
            mqttManager.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable cause) {

                }

                @Override
                public void messageArrived(String topic, MqttMessage message) throws Exception {
                    String msgcheck = new String(message.getPayload());
                    if (topic.equals(Topic_signupcheck)) {
                        if (msgcheck.equals("success")) {
                            Toast.makeText(SignUp_Activity.this, "Sign up success", Toast.LENGTH_SHORT).show();
                            Intent intent = new Intent(getApplicationContext(), HomeActivity.class);
                            intent.putExtra("username",username);
                            startActivity(intent);
                            finish();
                        } else if (msgcheck.equals("exist")) {
                            Toast.makeText(SignUp_Activity.this, "Username had already exist", Toast.LENGTH_SHORT).show();
                            usernameInput.setError("Username had already exist");
                            passwordInput.getText().clear();
                            passwordConfirm.getText().clear();
                        }
                    }
                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {

                }
            });
        }

    }
}
