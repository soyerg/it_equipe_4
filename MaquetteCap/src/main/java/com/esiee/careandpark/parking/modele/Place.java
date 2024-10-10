package com.esiee.careandpark.parking.modele;

import com.esiee.careandpark.parking.modele.reference.EtatPlace;
import com.esiee.careandpark.parking.modele.reference.TypePlace;

public class Place {
	
	private final TypePlace type;
	private EtatPlace etat;
	private int numero;
	
	public Place(TypePlace type,int numero) {
		this.type=type;
		this.etat=EtatPlace.Libre;
		this.numero = numero;
		
	}
	
	public TypePlace getType() {
		return type;
	}
	
	public EtatPlace getEtat() {
		return etat;
	}
	
	public void setEtat(EtatPlace etat) {
		this.etat=etat;
	}
	
	public int getNumero() {
		return this.numero;
	}

}
