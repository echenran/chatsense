package com.chatsense.chatsense;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Conversations extends AppCompatActivity implements View.OnClickListener{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_conversations);

        TextView username = (TextView) findViewById(R.id.username);

        Bundle extras = getIntent().getExtras();
        username.setText(extras.getString("user"));

        Button convo1 = (Button) findViewById(R.id.convo1);
        convo1.setOnClickListener(this);

    }

    public void onClick(View view)
    {
        Button b = (Button)view;
        Intent i = new Intent(this, Chat.class);
        i.putExtra("whose_mans",b.getText().toString());
        startActivity(i);
    }
}
