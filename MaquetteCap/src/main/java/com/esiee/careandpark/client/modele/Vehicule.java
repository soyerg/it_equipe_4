package com.esiee.careandpark.client.modele;

import com.esiee.careandpark.client.modele.reference.TypeVehicule;

public class Vehicule {

	private TypeVehicule type;

	public Vehicule(TypeVehicule type) {
		this.type = type;
	}

	public TypeVehicule getType() {
		return type;
	}

	public void setType(TypeVehicule type) {
		this.type = type;
	}

}
