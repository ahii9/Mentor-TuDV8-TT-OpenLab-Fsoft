package com.example.mqtt_app;

import static android.content.ContentValues.TAG;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity {
    private static final String Topic_data = "device/data";
    private static final String Topic_state = "device/connect_state";


    MqttManager mqttManager = MqttManager.getInstance(this);




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        initMqtt();
    }

    private void initMqtt() {
        connect();

    }
    //Ham xu ly ket noi voi mqtt
    private void connect() {
        mqttManager.connect(new IMqttActionListener() {
            @Override
            public void onSuccess(IMqttToken asyncActionToken) {
                // We are connected
                Log.d("MQTT", "onSuccess");
                Toast.makeText(MainActivity.this, "Connect success", Toast.LENGTH_SHORT).show();
                //them cac topic subscribe
                subTopic(Topic_data,0);
                subTopic(Topic_state,0);
                //
                startActivity(new Intent(MainActivity.this, HomeActivity.class));
//                startActivity(new Intent(MainActivity.this, Login_Activity.class));

                finish();
            }

            @Override
            public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                // Something went wrong e.g. connection timeout or firewall problems
                Log.d("MQTT", "onFailure",exception);
                setContentView(R.layout.loading_page);
            }
        });
    }

    public void connect(View view) {
        connect();
    }
    private void subTopic(String topic, int qos) {
        mqttManager.subscribe(topic, qos, new IMqttActionListener() {
            @Override
            public void onSuccess(IMqttToken asyncActionToken) {
                Log.d("Mqtt","Subscribe: "+ topic +" success");
            }

            @Override
            public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                exception.printStackTrace();
            }
        });
    }


}