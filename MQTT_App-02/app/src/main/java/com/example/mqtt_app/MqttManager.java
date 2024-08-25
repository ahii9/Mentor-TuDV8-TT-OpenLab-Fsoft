package com.example.mqtt_app;

import android.content.Context;
import android.widget.Toast;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MqttManager {
    private static MqttManager instance;
    private MqttAndroidClient mqttAndroidClient;

    private MqttManager(Context context) {
            String MQTT_BROKER_URL = "tcp://broker.hivemq.com:1883"; // Replace with your broker URL
        String CLIENT_ID = MqttClient.generateClientId();
        mqttAndroidClient = new MqttAndroidClient(context, MQTT_BROKER_URL, CLIENT_ID);
    }

    public static MqttManager getInstance(Context context) {
        if (instance == null) {
            instance = new MqttManager(context);
        }
        return instance;
    }

    public MqttAndroidClient getMqttClient() {
        return mqttAndroidClient;
    }

    public void connect(IMqttActionListener callback) {
        try {
            IMqttToken token = mqttAndroidClient.connect();
            token.setActionCallback(callback);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void publish(String topic, String payload) {
        if (mqttAndroidClient != null && mqttAndroidClient.isConnected()) {
            try {
                MqttMessage message = new MqttMessage();
                message.setPayload(payload.getBytes());
                mqttAndroidClient.publish(topic, message);
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    public void subscribe(String topic, int qos) {
        if (mqttAndroidClient != null && mqttAndroidClient.isConnected()) {
            try {
                mqttAndroidClient.subscribe(topic, qos, null);
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    public void setCallback(MqttCallback callback) {
        if (mqttAndroidClient != null) {
            mqttAndroidClient.setCallback(callback);
        }
    }
}
