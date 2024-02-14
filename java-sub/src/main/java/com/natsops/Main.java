package com.natsops;

public class Main {

    public static void main(String[] args) {
        
        NatsSubscriber subscriber = new NatsSubscriber(args[0]);
        subscriber.subscribeAsync(args[1]);
    }
}