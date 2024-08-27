package com.example.mqtt_app;

import  static android.content.ContentValues.TAG;

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

//import org.eclipse.paho.android.service.MqttAndroidClient;
import info.mqtt.android.service.MqttAndroidClient;

import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.internal.wire.MqttReceivedMessage;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class HomeActivity extends AppCompatActivity {

    private static final String Topic_data = "device/data";
    private static final String Topic_state = "device/connect_state";
    private String Topic_Lock = "device/lock";

//    private MqttMessageReceiver messageReceiver;
    private MqttManager mqttManager = MqttManager.getInstance(this);

    private String username ;

    private Button book,donebt;
    private Button open;

    private Boolean canOpen = false;
    private Boolean isBook = true;
    private Boolean canChange = true;

    private Button selectedButton = null;

    private List<Button_Manager> buttonList;
    List<String> listMsg;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        mqttManager.subscribe(Topic_data,1);
//        messageReceiver = new MqttMessageReceiver();
//
//        LocalBroadcastManager.getInstance(this).registerReceiver(messageReceiver, new IntentFilter("MQTT_MESS_RECEIVED"));
        username = getIntent().getStringExtra("username");
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
        open = findViewById(R.id.openButton);

        for (Button_Manager button : buttonList) {
            button.getButton().setEnabled(false);
        }
        if (!canOpen) {
            open.setEnabled(false);
            open.setVisibility(View.INVISIBLE);
        } else {
            open.setEnabled(true);
            open.setVisibility(View.VISIBLE);
        }


        donebt.setEnabled(false);
        donebt.setVisibility(View.INVISIBLE);
        book.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(isBook) {
                    isBook = false;
                    canChange =false;
                    canOpen = false;
                    book.setText("Back");
                    donebt.setVisibility(View.VISIBLE);
                    donebt.setBackgroundColor(Color.parseColor("#7DE981"));
                    donebt.setEnabled(true);
                    lock_area();
//                    }
                } else {
                    isBook = true;
                    canChange = true;
                    canOpen = true;
                    book.setText("Book");
                    for (Button_Manager button : buttonList) {
                        button.getButton().setEnabled(false);
                    }
                    donebt.setEnabled(false);
                    book.setEnabled(true);
                    donebt.setVisibility(View.INVISIBLE);
                }
            }
        });
        donebt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                for (Button_Manager button : buttonList) {
                    button.getButton().setEnabled(false);
                }
                donebt.setEnabled(false);
                book.setEnabled(true);
                donebt.setVisibility(View.INVISIBLE);
                pub_LockTopic();
//                hadChange = false;
                isBook = true;
                canChange = true;
                book.setText("Book");
            }
        });
        open.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                for (Button_Manager buttonManager :buttonList) {
                    if (buttonManager.getState().equals(username)) {
                        buttonManager.setState("CLEAR");
                        selectedButton = null;
                    }
                }
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
                        listMsg = dataReceived(messageReceived);
                        Log.d(TAG,"message: " +new String(message.getPayload()));
                        if (canChange) {
                            changeGUI();
                            for (Button_Manager buttonManager : buttonList) {
                                if (buttonManager.getState().equals(username)) {
                                    canOpen = true;
                                    break;
                                }
                                canOpen = false;
                            }
                        }

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
    public void changeGUI() {

        for (int i =0; i< 3; i++) {
            if(listMsg.get(i).equals("HAD_CAR")) {
                buttonList.get(i).setState("HAD_CAR");
            } else if (listMsg.get(i).equals("CLEAR")){
                buttonList.get(i).setState("CLEAR");
            } else {
                buttonList.get(i).setState(listMsg.get(i));
            }

            buttonList.get(i).buttonChange();
        }

    }
//
    private void lock_area() {
        for (Button_Manager buttonManager :buttonList) {
            if (buttonManager.getState().equals(username)) {
                selectedButton = buttonManager.getButton();
            }
        }
        for (Button_Manager buttonManager : buttonList) {
            buttonManager.getButton().setEnabled(true);

            if (buttonManager.getState().equals(username)) {
                selectedButton = buttonManager.getButton();
            }
            buttonManager.getButton().setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    if (buttonManager.getState().equals("CLEAR")) {
                        if (selectedButton !=null) {
                            Toast.makeText(HomeActivity.this, "Can choose only 1", Toast.LENGTH_SHORT).show();
                        } else {
                            selectedButton = buttonManager.getButton();
                            buttonManager.setState(username);
                        }
                    } else if (buttonManager.getState().equals(username)){
                        buttonManager.setState("CLEAR");
                        selectedButton = null;
                    }
                    buttonManager.buttonChange();
                }

            });


        }
    }
    private void pub_LockTopic() {
        String msg ="";
        for (Button_Manager buttonManager : buttonList) {
            msg += buttonManager.getState()+"/";
        }
        msg = msg.substring(0,msg.length()-1);
        mqttManager.publish(Topic_Lock, msg);
//        Toast.makeText(this, "pub success", Toast.LENGTH_SHORT).show();
    }
    private List<String>  dataReceived(String msg) {
        List<String> list = Arrays.asList(msg.split("/"));
        return list;
    }
}
