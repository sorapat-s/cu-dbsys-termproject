console.log("loaded script");

var cell = null;
var entryID = "";
var attrbID = "";
var oldData = "";
var newData = "";

const VALIDATTRB = [
  "trip_id",
  "tour_program_id",
  "start_date",
  "end_date",
  "number_of_customer",
  "reservation_start",
  "reservation_end",
  "price",
];
const NOTNULLATTRB = [
  "trip_id",
  "tour_program_id",
  "start_date",
  "end_date",
  "number_of_customer",
  "reservation_start",
  "reservation_end",
  "price",
];
const APIPATH = "/api/data/trip";

const tableDiv = document.getElementById("table");
const addButton = document.getElementById("addbutton");
const addModal = document.getElementById("addmodal");
const addForm = document.getElementById("addform");
const addClose = document.getElementById("addclose");
const editModal = document.getElementById("editmodal");
const editText = document.getElementById("edittext");
const editConfirm = document.getElementById("editconfirm");
const editCancel = document.getElementById("editcancel");
const editClose = document.getElementById("editclose");
const deleteModal = document.getElementById("deletemodal");
const deleteConfirm = document.getElementById("deleteconfirm");
const deleteCancel = document.getElementById("deletecancel");
const deleteClose = document.getElementById("deleteclose");

const updateUrl = (prev, query) => {
  return (
    prev +
    (prev.indexOf("?") >= 0 ? "&" : "?") +
    new URLSearchParams(query).toString()
  );
};

const editableCellAttributes = (data, row, col) => {
  if (row) {
    return {
      contentEditable: "true",
      "data-element-id": row.cells[0].data,
      customerID: row.cells[0].data,
    };
  } else {
    return {};
  }
};

var grid = new gridjs.Grid({
  columns: [
    { id: "trip_id", name: "Trip ID" },
    {
      id: "tour_program_id",
      name: "Tour Program ID",
      attributes: editableCellAttributes,
    },
    {
      id: "start_date",
      name: "Start Date",
      attributes: editableCellAttributes,
    },
    {
      id: "end_date",
      name: "End Date",
      attributes: editableCellAttributes,
    },
    {
      id: "number_of_customer",
      name: "#Customer",
      attributes: editableCellAttributes,
    },
    {
      id: "reservation_start",
      name: "Start Reservation",
      attributes: editableCellAttributes,
    },
    {
      id: "reservation_end",
      name: "End Reservation",
      attributes: editableCellAttributes,
    },
    { id: "price", name: "Price", attributes: editableCellAttributes },
    {
      id: "actions",
      sort: false,
      formatter: (cell, row) =>
        gridjs.html(
          `<button type="button" onclick="triggerDelete(${row.cells[0].data})">Delete</button> <button type="button" onclick="generateReport(${row.cells[0].data})">Generate Report</button>`
        ),
    },
  ],
  server: {
    url: APIPATH,
    then: (results) => results.data,
    total: (results) => results.total,
  },
  search: {
    enabled: true,
    server: {
      url: (prev, search) => {
        return updateUrl(prev, { search });
      },
    },
  },
  sort: {
    enabled: true,
    multiColumn: true,
    server: {
      url: (prev, columns) => {
        const columnIds = [
          "trip_id",
          "tour_program_id",
          "start_date",
          "end_date",
          "number_of_customer",
          "reservation_start",
          "reservation_end",
          "price",
        ];
        const sort = columns.map(
          (col) => (col.direction === 1 ? "+" : "-") + columnIds[col.index]
        );
        return updateUrl(prev, { sort });
      },
    },
  },
  pagination: {
    enabled: true,
    server: {
      url: (prev, page, limit) => {
        return updateUrl(prev, { start: page * limit, length: limit });
      },
    },
  },
});

grid.render(tableDiv);

function resetVar() {
  cell = null;
  entryID = "";
  oldData = "";
  newData = "";
  attrbID = "";
}

function requestAdd(event) {
  console.log("called request add");
  eventdata = new FormData(event.target);
  eventdata.append("type", "add");
  eventdata.append("id", "-2");
  fetch(APIPATH, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(Object.fromEntries(eventdata)),
  });
  addModal.close();
  grid.forceRender();
}

function requestEdit() {
  fetch(APIPATH, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: entryID,
      type: "edit",
      [attrbID]: newData,
    }),
  });
  resetVar();
  editModal.close();
}

function cancelEdit() {
  if (cell) {
    cell.textContent = oldData;
  }

  resetVar();
  editModal.close();
}

function triggerEdit() {
  if (cell === null) {
    alert("Cell is null.");
  } else if (entryID === "") {
    alert("Entry ID is null.");
  } else if (attrbID === "") {
    alert("Attribute ID is null.");
  } else if (NOTNULLATTRB.includes(attrbID) && oldData === "") {
    alert("Previous value is null.");
  } else if (!VALIDATTRB.includes(attrbID)) {
    alert("Invalid Attribute.");
  } else if (NOTNULLATTRB.includes(attrbID) && newData === "") {
    alert("Attribute cannot be null.");
  } else {
    editText.innerText = `Change "${oldData}" to "${newData}"`;
    editModal.showModal();
  }
}

function requestDelete() {
  fetch(APIPATH, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: entryID,
      type: "delete",
    }),
  });
  deleteModal.close();
  grid.forceRender();
}

function cancelDelete() {
  deleteModal.close();
  resetVar();
}

function triggerDelete(entryIDdelete) {
  if (entryIDdelete === "") {
    alert("Entry ID is null.");
  } else {
    entryID = entryIDdelete;
    deleteModal.showModal();
  }
}
function generateReport(trip_id) {
  window.location.href = `/trip_report/${trip_id}`;
}

let savedValue;

tableDiv.addEventListener("focusin", (ev) => {
  if (ev.target.tagName === "TD") {
    savedValue = ev.target.textContent;
  }
});

tableDiv.addEventListener("focusout", (ev) => {
  if (ev.target.tagName === "TD") {
    if (savedValue !== ev.target.textContent) {
      resetVar();
      cell = ev.target;
      console.log(cell);
      console.log(ev.target.attributes.customerID);
      entryID = ev.target.dataset.elementId;
      attrbID = ev.target.dataset.columnId;
      oldData = savedValue;
      newData = ev.target.textContent;
      console.log("trigger edit");
      triggerEdit();
    }
    savedValue = undefined;
  }
});

tableDiv.addEventListener("keydown", (ev) => {
  if (ev.target.tagName === "TD") {
    if (ev.key === "Escape") {
      ev.target.textContent = savedValue;
      ev.target.blur();
    } else if (ev.key === "Enter") {
      ev.preventDefault();
      ev.target.blur();
    }
  }
});

addButton.addEventListener("click", (ev) => {
  addModal.showModal();
});

addForm.addEventListener("submit", (ev) => {
  ev.preventDefault();
  requestAdd(ev);
});

addClose.addEventListener("click", (ev) => {
  addModal.close();
});

editCancel.addEventListener("click", (ev) => {
  cancelEdit();
});

editClose.addEventListener("click", (ev) => {
  cancelEdit();
});

editConfirm.addEventListener("click", (ev) => {
  requestEdit();
});

deleteCancel.addEventListener("click", (ev) => {
  cancelDelete();
});

deleteClose.addEventListener("click", (ev) => {
  cancelDelete();
});

deleteConfirm.addEventListener("click", (ev) => {
  requestDelete();
});
