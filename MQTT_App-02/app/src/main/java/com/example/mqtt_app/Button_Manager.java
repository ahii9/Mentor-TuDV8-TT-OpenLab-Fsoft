package com.example.mqtt_app;

import android.graphics.Color;
import android.widget.Button;

public class Button_Manager {
    private final static int CLEAR = 0;
    private final static int HAD_CAR = 1;
    private final static int LOCKED = 2;

    private int state;
    private Button button;

    public Button_Manager(Button button) {
        this.button = button;
        this.state = CLEAR;
    }

    public int getState() {
        return state;
    }

    public void setState(int state) {
        this.state = state;
    }

    public Button getButton() {
        return button;
    }

    public void buttonChange() {
        switch (state) {
            case CLEAR:
                button.setBackgroundColor(Color.parseColor("#EEEEEE"));
                break;
            case HAD_CAR:
                button.setBackgroundColor(Color.parseColor("#EB6666"));
                break;
            case LOCKED:
                button.setBackgroundColor(Color.parseColor("#FF9800"));
                break;
        }
    }
}
