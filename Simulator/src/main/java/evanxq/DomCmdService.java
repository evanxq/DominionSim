package evanxq;

import be.aga.dominionSimulator.DomEngine;
import be.aga.dominionSimulator.DomGame;
import be.aga.dominionSimulator.DomPlayer;
import be.aga.dominionSimulator.XMLHandler;
import org.xml.sax.InputSource;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;


import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Created by Evan on 1/20/2017.
 */
public class DomCmdService {

    private static String handleGame(String input) {
        ArrayList<DomPlayer> players = new ArrayList<>();

        try {
            InputSource is = new InputSource(new StringReader(input));
            XMLHandler hnd = new XMLHandler();
            XMLReader rdr = XMLReaderFactory.createXMLReader();
            rdr.setContentHandler(hnd);
            rdr.parse(is);
            players = hnd.getBots();
            //System.out.println("has " + players.size() + " players");
        } catch (Exception e) {
            e.printStackTrace();
        }

        int nTestGames = 10;
        DomEngine headlessEngine = new DomEngine(false);
        //System.out.println("starting simulation");
        headlessEngine.startSimulation(players, false, nTestGames, false);
        //System.out.println("ending simulation");

        String out = "";
        for(DomPlayer p : players) {
            out += " " + p.getWins();
        }
        //System.out.println("returning " + out.trim());
        return out.trim() + "\n";
    }

    public static void main(String[] args) {
        try (
                ServerSocket serverSocket = new ServerSocket(22222);
                Socket clientSocket = serverSocket.accept();
                PrintWriter out =
                        new PrintWriter(clientSocket.getOutputStream(), true);
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(clientSocket.getInputStream()))
        ) {
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                out.println( handleGame(inputLine) );
            }
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen");
            System.out.println(e.getMessage());
        }

    }

}
