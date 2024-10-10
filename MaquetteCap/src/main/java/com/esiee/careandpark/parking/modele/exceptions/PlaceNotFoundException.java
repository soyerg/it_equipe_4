package com.esiee.careandpark.parking.modele.exceptions;

public class PlaceNotFoundException extends Exception{

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	public PlaceNotFoundException(int numero) {
		super("la place "+numero+" n'existe pas");
	}
	
	

}
