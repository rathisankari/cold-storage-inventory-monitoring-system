import { useEffect, useState } from "react";
import api from "../services/api";
import "../App.css";

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [error, setError] = useState("");

  const [vaccineName, setVaccineName] = useState("");
  const [vaccineCode, setVaccineCode] = useState("");
  const [lotNumber, setLotNumber] = useState("");
  const [quantity, setQuantity] = useState("");
  const [expirationDate, setExpirationDate] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editQuantity, setEditQuantity] = useState("");

  useEffect(() => {
    api
      .get("/inventory/")
      .then((response) => {
        setInventory(response.data);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load inventory");
      });
  }, []);

  const handleCreate = (event) => {
    event.preventDefault();

    const newInventory = {
      storage_unit_id: 3,
      vaccine_name: vaccineName,
      vaccine_code: vaccineCode,
      lot_number: lotNumber,
      quantity: Number(quantity),
      expiration_date: expirationDate,
      status: "Good",
    };

    api
      .post("/inventory/", newInventory)
      .then((response) => {
        setInventory((currentInventory) => [
          ...currentInventory,
          response.data,
        ]);

        setVaccineName("");
        setVaccineCode("");
        setLotNumber("");
        setQuantity("");
        setExpirationDate("");
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to create inventory");
      });
  };

  const handleUpdate = (item) => {
    const updatedInventory = {
      storage_unit_id: item.storage_unit_id,
      vaccine_name: item.vaccine_name,
      vaccine_code: item.vaccine_code,
      lot_number: item.lot_number,
      quantity: Number(editQuantity),
      expiration_date: item.expiration_date,
    };

    api
      .put(`/inventory/${item.id}`, updatedInventory)
      .then((response) => {
        setInventory((currentInventory) =>
          currentInventory.map((inventoryItem) =>
            inventoryItem.id === item.id ? response.data : inventoryItem
          )
        );

        setEditingId(null);
        setEditQuantity("");
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to update inventory");
      });
  };

  const handleCompromise = (item) => {
    api
      .patch(`/inventory/${item.id}/status`, {
        status: "Compromised",
      })
      .then((response) => {
        setInventory((currentInventory) =>
          currentInventory.map((inventoryItem) =>
            inventoryItem.id === item.id ? response.data : inventoryItem
          )
        );
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to mark inventory as compromised");
      });
  };

  const startEditing = (item) => {
    setEditingId(item.id);
    setEditQuantity(item.quantity);
  };

  if (error) {
    return <div className="page-message">{error}</div>;
  }

  return (
    <div className="inventory-page">
      <main className="inventory-content">

        <section className="inventory-header">
          <div>
            <span className="section-label">Inventory Management</span>
            <h1>Inventory</h1>
            <p>
              Manage vaccines stored in the cold storage unit.
            </p>
          </div>
        </section>

        <section className="inventory-form-section">
          <div className="section-header">
            <div>
              <span className="section-label">Inventory</span>
              <h2>Add Inventory</h2>
            </div>
          </div>

          <form className="inventory-form" onSubmit={handleCreate}>

            <div className="form-group">
              <label>Vaccine Name</label>

              <input
                type="text"
                placeholder="e.g. Covaxin"
                value={vaccineName}
                onChange={(event) =>
                  setVaccineName(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Vaccine Code</label>

              <input
                type="text"
                placeholder="e.g. COV-002"
                value={vaccineCode}
                onChange={(event) =>
                  setVaccineCode(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Lot Number</label>

              <input
                type="text"
                placeholder="e.g. LOT-2026-002"
                value={lotNumber}
                onChange={(event) =>
                  setLotNumber(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Quantity</label>

              <input
                type="number"
                min="0"
                placeholder="Quantity"
                value={quantity}
                onChange={(event) =>
                  setQuantity(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Expiration Date</label>

              <input
                type="date"
                value={expirationDate}
                onChange={(event) =>
                  setExpirationDate(event.target.value)
                }
                required
              />
            </div>

            <button
              className="primary-button"
              type="submit"
            >
              Add Inventory
            </button>

          </form>
        </section>

        <section className="inventory-records-section">

          <div className="section-header">
            <div>
              <span className="section-label">Records</span>
              <h2>Inventory Records</h2>
            </div>

            <span className="record-count">
              {inventory.length}
            </span>
          </div>

          <div className="inventory-grid">

            {inventory.map((item) => (

              <div
                className="inventory-card"
                key={item.id}
              >

                <div className="inventory-card-header">

                  <div>
                    <h3>{item.vaccine_name}</h3>

                    <span>
                      Inventory ID: {item.id}
                    </span>
                  </div>

                  <span
                    className={`inventory-status ${item.status
                      .toLowerCase()
                      .replace(" ", "-")}`}
                  >
                    {item.status}
                  </span>

                </div>

                <div className="inventory-details">

                  <div>
                    <span>Code</span>
                    <strong>{item.vaccine_code}</strong>
                  </div>

                  <div>
                    <span>Lot Number</span>
                    <strong>{item.lot_number}</strong>
                  </div>

                  <div>
                    <span>Quantity</span>
                    <strong>{item.quantity}</strong>
                  </div>

                  <div>
                    <span>Expiry</span>
                    <strong>{item.expiration_date}</strong>
                  </div>

                </div>

                {editingId === item.id ? (

                  <div className="edit-section">

                    <input
                      type="number"
                      min="0"
                      value={editQuantity}
                      onChange={(event) =>
                        setEditQuantity(event.target.value)
                      }
                    />

                    <div className="button-group">

                      <button
                        className="primary-button"
                        onClick={() => handleUpdate(item)}
                      >
                        Save Changes
                      </button>

                      <button
                        className="secondary-button"
                        onClick={() => {
                          setEditingId(null);
                          setEditQuantity("");
                        }}
                      >
                        Cancel
                      </button>

                    </div>

                  </div>

                ) : (

                  <div className="button-group">

                    <button
                      className="secondary-button"
                      onClick={() => startEditing(item)}
                    >
                      Edit
                    </button>

                    {item.status !== "Compromised" && (
                      <button
                        className="secondary-button"
                        onClick={() => handleCompromise(item)}
                      >
                        Mark as Compromised
                      </button>
                    )}

                  </div>

                )}

              </div>

            ))}

          </div>

        </section>

      </main>
    </div>
  );
}

export default Inventory; 