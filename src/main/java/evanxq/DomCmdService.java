package evanxq;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Created by Evan on 1/20/2017.
 */
public class DomCmdService {

    public static void main(String[] args) {
        if(args.length == 0) {
            System.out.println("hello world");
        }

        try (
                ServerSocket serverSocket = new ServerSocket(22222);
                Socket clientSocket = serverSocket.accept();
                PrintWriter out =
                        new PrintWriter(clientSocket.getOutputStream(), true);
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(clientSocket.getInputStream()))
        ) {

            String inputLine, outputLine;

            while ((inputLine = in.readLine()) != null) {
                outputLine = inputLine;
                System.out.println(inputLine);
                out.println(outputLine);
            }
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen");
            System.out.println(e.getMessage());
        }

    }

}
