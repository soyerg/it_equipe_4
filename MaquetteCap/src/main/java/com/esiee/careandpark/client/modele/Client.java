package com.esiee.careandpark.client.modele;

import com.esiee.careandpark.parking.services.ParkingServiceForClient;

public class Client {

	private String nom;
	private Vehicule vehicule;

	public String getNom() {
		return nom;
	}

	public void setNom(String nom) {
		this.nom = nom;
	}

	/**
	 * Renvoie le nomnbre de place pour un parking donné qui correspondent au véhicule du client
	 */
	public int chercherUnePlace(String parkingName) {
		ParkingServiceForClient parkingServiceForClient = new ParkingServiceForClient();
		parkingServiceForClient.recherchePlace("", vehicule.getType()
			.getTypePlace());
		return 0;
	}

}
