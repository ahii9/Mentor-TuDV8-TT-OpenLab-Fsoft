package com.example.mqtt_app;

import android.graphics.Color;
import android.widget.Button;

public class Button_Manager {

    private String state;
    private Button button;

    public Button_Manager(Button button) {
        this.button = button;
        this.state = "CLEAR";
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public Button getButton() {
        return button;
    }

    public void buttonChange() {
        switch (state) {
            case "CLEAR":
                button.setBackgroundColor(Color.parseColor("#EEEEEE"));
                break;
            case "HAD_CAR":
                button.setBackgroundColor(Color.parseColor("#EB6666"));
                break;
            case "LOCKED":
                button.setBackgroundColor(Color.parseColor("#FF9800"));
                break;
        }
    }
}
