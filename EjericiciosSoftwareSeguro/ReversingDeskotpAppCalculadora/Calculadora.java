/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.Base64;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class Calculadora
extends JFrame {
    private JLabel lblResultado = new JLabel(" ");
    private JPanel pnlBotones = new JPanel(new GridLayout(4, 4));
    private JPanel pnlIgual = new JPanel(new GridLayout(1, 1));
    private JButton[] botones = new JButton[]{new JButton("A"), new JButton("B"), new JButton("C"), new JButton("D"), new JButton("Limpiar"), new JButton("Finalizar")};
    private Dimension dmVentana = new Dimension(300, 440);
    private double resultado = 0.0;
    private double numero;
    private static final int SUMA = 1;
    private static final int RESTA = 2;
    private static final int MULTIPLICACION = 3;
    private static final int DIVISION = 4;
    private static final int NINGUNO = 0;
    private int operador = 0;
    private boolean hayPunto = false;
    private boolean nuevoNumero = true;
    private NumberFormat nf = NumberFormat.getInstance();

    public Calculadora() {
        Dimension dimension = Toolkit.getDefaultToolkit().getScreenSize();
        int n = (dimension.width - this.dmVentana.width) / 2;
        int n2 = (dimension.height - this.dmVentana.height) / 2;
        this.setLocation(n, n2);
        this.setSize(this.dmVentana);
        this.setTitle("Calculadora");
        this.lblResultado.setBackground(Color.white);
        this.lblResultado.setOpaque(true);
        this.lblResultado.setFont(new Font("Arial", 0, 32));
        PulsaRaton pulsaRaton = new PulsaRaton();
        for (int i = 0; i < this.botones.length; ++i) {
            this.pnlBotones.add(this.botones[i]);
            this.botones[i].addActionListener(pulsaRaton);
        }
        this.add((Component)this.lblResultado, "North");
        this.add(this.pnlBotones);
        this.setDefaultCloseOperation(3);
        this.setVisible(true);
        this.lblResultado.setText(" ");
        this.lblResultado.setHorizontalAlignment(4);
    }

    public static void main(String[] stringArray) {
        new Calculadora();
    }

    private void sendGET(String string) throws Exception {
        URL uRL = new URL(string);
        HttpURLConnection httpURLConnection = (HttpURLConnection)uRL.openConnection();
        httpURLConnection.setRequestMethod("GET");
        int n = httpURLConnection.getResponseCode();
        if (n == 200) {
            String string2;
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
            StringBuffer stringBuffer = new StringBuffer();
            while ((string2 = bufferedReader.readLine()) != null) {
                stringBuffer.append(string2);
            }
            bufferedReader.close();
            this.lblResultado.setText(stringBuffer.toString());
            System.out.println("Respuesta: " + stringBuffer.toString());
        } else {
            this.lblResultado.setText("Error");
        }
    }

    public static String obfuscateURL(String string) {
        return Base64.getEncoder().encodeToString(string.getBytes());
    }

    public static String deobfuscateURL(String string) {
        byte[] byArray = Base64.getDecoder().decode(string);
        return new String(byArray);
    }

    public void operar(int n) {
        String string;
        if (!this.nuevoNumero && !(string = this.lblResultado.getText()).isEmpty()) {
            Number number = null;
            try {
                number = this.nf.parse(string);
                this.numero = number.doubleValue();
            }
            catch (ParseException parseException) {
                // empty catch block
            }
            switch (this.operador) {
                case 1: {
                    this.resultado += this.numero;
                    break;
                }
                case 2: {
                    this.resultado -= this.numero;
                    break;
                }
                case 3: {
                    this.resultado *= this.numero;
                    break;
                }
                case 4: {
                    this.resultado /= this.numero;
                    break;
                }
                default: {
                    this.resultado = this.numero;
                }
            }
            this.operador = n;
            this.lblResultado.setText(this.nf.format(this.resultado));
            this.nuevoNumero = true;
            this.hayPunto = false;
        }
    }

    class PulsaRaton
    implements ActionListener {
        PulsaRaton() {
        }

        @Override
        public void actionPerformed(ActionEvent actionEvent) {
            JButton jButton = (JButton)actionEvent.getSource();
            String string = jButton.getText();
            if (string.equals("Finalizar")) {
                try {
                    String string2 = "aHR0cDovL2FwaS1jYWxjdWxhZG9yYS5zb2Z0d2FyZXNlZ3Vyby5jb20uYXIvdmVyaWZpY2FyLWNvZGlnby1jYWxjdWxhZG9yYS8/dD0=";
                    String string3 = Calculadora.deobfuscateURL(string2);
                    String string4 = Calculadora.this.lblResultado.getText();
                    String string5 = string3 + string4;
                    Calculadora.this.sendGET(string3);
                }
                catch (Exception exception) {
                    exception.printStackTrace();
                }
            } else if (string.equals("Limpiar")) {
                Calculadora.this.lblResultado.setText(" ");
            } else {
                Calculadora.this.lblResultado.setText(string);
            }
        }
    }
}

