package com.esiee.careandpark.parking.services;

import com.esiee.careandpark.parking.modele.exceptions.ParkingNotFoundException;
import com.esiee.careandpark.parking.modele.exceptions.PlaceNotFoundException;
import com.esiee.careandpark.parking.modele.reference.TypePlace;

public class ParkingServiceForClient {
	
	
	public ParkingServiceForClient() {
		
	}
	
	
	/**
	 * reserve une place de numéro numero dans le parking
	 * @param parkingName
	 * @param numero
	 * @throws ParkingNotFoundException si le parking n'existe pas
	 * @throws PlaceNotFoundException si la place n'existe pas dans le parking
	 */
	public void stationner(String parkingName,int numero) throws ParkingNotFoundException, PlaceNotFoundException{
		throw new ParkingNotFoundException(parkingName);
	}
	
	/**
	 * libere une place de numéro numero dans le parking
	 * @param parkingName
	 * @param numero
	 */
	public void libererPlace(String parkingName,int numero) {
		
	}
	
	/**
	 * rercherche une place dans un parking pour un type de place donné
	 * @param parkingName
	 * @param typePlace
	 */
	public void recherchePlace(String parkingName,TypePlace typePlace) {
		
	}
	

}
