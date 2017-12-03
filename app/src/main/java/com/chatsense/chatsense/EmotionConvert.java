package com.chatsense.chatsense;


import android.graphics.Color;

/**
 * Created by Jacob on 2017-12-02.
 */

public class EmotionConvert {

    private Color color;

    public Color getColorFromValues(int neutral, int happy, int sad, int angry, int fear)
    {
       color = Color.valueOf((angry+happy/2 + neutral)/100,(fear+happy/2 + neutral)/100,(sad+neutral)/100);

        return color;
    }

    public String getEmojiFromValues(int neutral, int happy, int sad, int angry, int fear)
    {
        String NEUTRAL = "";

        String SAD3 = "";
        String SAD2 = "";
        String SAD1 = "";

        String FEAR3 = "";
        String FEAR2 = "";
        String FEAR1 = "";

        String HAPPY3 = "";
        String HAPPY2 = "";
        String HAPPY1 = "";

        String ANGRY3 = "";
        String ANGRY2 = "";
        String ANGRY1 = "";

        if (neutral > 75)
        {

        }


        return "";
    }

}
