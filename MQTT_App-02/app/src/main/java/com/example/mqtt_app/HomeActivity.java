package com.example.mqtt_app;

import static android.content.ContentValues.TAG;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Vibrator;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.internal.wire.MqttReceivedMessage;

import java.util.ArrayList;
import java.util.List;

public class HomeActivity extends AppCompatActivity {
    private final static int CLEAR = 0;
    private final static int HAD_CAR = 1;
    private final static int LOCKED = 2;
    private static final String Topic_data = "device/data";
    private static final String Topic_state = "device/connect_state";
    private String Topic_Lock = "device/lock";
//    private MqttMessageReceiver messageReceiver;
    private MqttManager mqttManager = MqttManager.getInstance(this);

    private Button areaA;
    private Button areaB;
    private Button areaC;
    private Button book,donebt;

    private List<Button_Manager> buttonList;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
//        messageReceiver = new MqttMessageReceiver();
//
//        LocalBroadcastManager.getInstance(this).registerReceiver(messageReceiver, new IntentFilter("MQTT_MESS_RECEIVED"));
        init();
        initMqtt();

    }
    private void init() {
        buttonList = new ArrayList<>();
        buttonList.add(new Button_Manager(findViewById(R.id.buttonA)));
        buttonList.add(new Button_Manager(findViewById(R.id.buttonB)));
        buttonList.add(new Button_Manager(findViewById(R.id.buttonC)));

        book = findViewById(R.id.book_button);
        donebt = findViewById(R.id.done_button);

        for (Button_Manager button : buttonList) {
            button.getButton().setEnabled(false);
        }
        donebt.setEnabled(false);
        donebt.setVisibility(View.INVISIBLE);
        book.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                donebt.setVisibility(View.VISIBLE);
                donebt.setEnabled(true);
                lock_area();
            }
        });
        donebt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                for (Button_Manager button : buttonList) {
                    button.getButton().setEnabled(false);
                }
                donebt.setEnabled(false);
                donebt.setVisibility(View.INVISIBLE);
                pub_LockTopic();

            }
        });
    }

    private void initMqtt() {

        if (mqttManager != null) {
            mqttManager.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable cause) {

                }

                @Override
                public void messageArrived(String topic, MqttMessage message) throws Exception {
//                    Log.d(TAG,"topic: " + topic);
//                    Log.d(TAG,"message: " +new String(message.getPayload()));
                    String messageReceived = new String(message.getPayload());
                    if (topic.equals(Topic_data)) {
                        changeGUI(messageReceived);
                    }

                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {

                }
            });
        } else {
            Log.d("HomeActivity", "MqttManager instance is null");
        }

    }
    public void changeGUI(String message) {

        for (int i =0; i< 3; i++) {
            if(message.charAt(i) == '1') {
                buttonList.get(i).setState(HAD_CAR);
            } else if (message.charAt(i) == '0'){
                buttonList.get(i).setState(CLEAR);
            } else {
                buttonList.get(i).setState(LOCKED);
            }
            buttonList.get(i).buttonChange();
        }

    }
//
    private void lock_area() {
        for (Button_Manager button : buttonList) {
            button.getButton().setEnabled(true);
            button.getButton().setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (button.getState() == CLEAR) {
                        button.setState(LOCKED);
                    } else if (button.getState() == LOCKED){
                        button.setState(CLEAR);
                    }
                    button.buttonChange();
                }
            });
        }
    }
    private void pub_LockTopic() {
        String msg ="";
        for (Button_Manager buttonManager : buttonList) {
            msg += buttonManager.getState();
        }
        mqttManager.publish(Topic_Lock, msg, new IMqttActionListener() {
            @Override
            public void onSuccess(IMqttToken asyncActionToken) {
                Log.d(TAG,"Pub Success: ");
            }

            @Override
            public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                Log.d(TAG,"Pub Failed");
            }
        });
    }
}
