package com.natsops;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.logging.Level;
import java.util.logging.Logger;

import io.nats.client.Connection;
import io.nats.client.Dispatcher;
import io.nats.client.Nats;

public final class NatsSubscriber {

    private static Logger LOGGER = Logger.getLogger(NatsSubscriber.class.getName());

    private final String serverURI;
    private final Connection natsConnection;

    NatsSubscriber(final String serverURI) {

        if (serverURI != null && !serverURI.isEmpty()) {
            this.serverURI = serverURI;
        } else {
            this.serverURI = "http://localhost:8082";
        }
        natsConnection = initConnection(this.serverURI);
    }

    private Connection initConnection(String serverURI) {

        try {
            // Will implement any error handling or authentication mechanism later
            return Nats.connectReconnectOnConnect(serverURI);
        } catch (IOException | InterruptedException ex) {
            LOGGER.log(Level.WARNING, "Error connecting to the NATS server.", ex);
            Thread.currentThread().interrupt();
            return null;
        }
    }

    public void subscribeAsync(final String subject) {
 
        try {
        
            Dispatcher subjectDispatcher = natsConnection.createDispatcher(message -> {
                final StringBuilder builder = new StringBuilder();
                builder.append("Received a message on '");
                builder.append(message.getSubject()).append("': ");
                builder.append(new String(message.getData(), StandardCharsets.UTF_8));
                
                LOGGER.log(Level.INFO, builder.toString());
            });
            
            if (subjectDispatcher == null) {
                LOGGER.log(Level.WARNING, "Dispatcher is null.");
            } else {
                subjectDispatcher.subscribe(subject);
            }
            
            // Sleep this thread a little so the dispatcher thread has time
            // to receive all the messages before the program quits.
            Thread.sleep(200);
        } catch (InterruptedException ex) {
            LOGGER.log(Level.WARNING, "Dispatcher thread interrupted.", ex);
            Thread.currentThread().interrupt();
        }
    }
}
