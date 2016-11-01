package mp2_java;

import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;

public class main {
	
	static ArrayList<autor> autores = new ArrayList<autor>();
	
	static Hashtable<String,String> textosTreino;
	

	public main(String[] args) {
		textosTreino.put("pg22615.txt","AlmadaNegreiros");
		treino();

	}
	
	public static void treino(){
		boolean flag = false;
		normalizar();
		Enumeration<String> txts = textosTreino.keys();
		while(txts.hasMoreElements()){
		    String text = ((Enumeration<String>) textosTreino).nextElement();
		    String aut = textosTreino.get(text);
		    for(autor a: autores){
		    	if(a.getNome() == aut){
		    		flag = true;	
		       	}
		    	a.addTexto(text);
		    }
		    if(flag == false){
		    	autor a = null;
		    	a.setNome(text);
		    	autores.add(a);
		    }
			
		}
	
	}
	
	public static void normalizar(){
		
	}

}