console.log("loaded script");

var cell = null;
var entryID = "";
var attrbID = "";
var oldData = "";
var newData = "";

const VALIDATTRB = [
  "tour_program_id",
  "tour_program_name",
  "max_number_of_customer",
  "destination_city",
  "destination_country",
  "duration",
  "min_price",
  "max_price",
  "tour_detail",
  "airline",
];
const NOTNULLATTRB = [
  "tour_program_id",
  "tour_program_name",
  "max_number_of_customer",
  "destination_city",
  "destination_country",
  "duration",
  "min_price",
  "max_price",
  "tour_detail",
  "airline",
];
const APIPATH = "/api/data/tour_program";

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
      tourID: row.cells[0].data,
    };
  } else {
    return {};
  }
};

var grid = new gridjs.Grid({
  columns: [
    { id: "tour_program_id" },
    {
      id: "tour_program_name",
      name: "Name",
      attributes: editableCellAttributes,
    },
    {
      id: "max_number_of_customer",
      name: "Max Customer",
      attributes: editableCellAttributes,
    },
    {
      id: "destination_city",
      name: "Destination City",
      attributes: editableCellAttributes,
    },
    {
      id: "destination_country",
      name: "Country",
      attributes: editableCellAttributes,
    },
    { id: "duration", name: "Duration", attributes: editableCellAttributes },
    { id: "min_price", name: "Min Price", attributes: editableCellAttributes },
    { id: "max_price", name: "Max Price", attributes: editableCellAttributes },
    {
      id: "tour_detail",
      name: "Tour Detail",
      attributes: editableCellAttributes,
    },
    { id: "airline", name: "Airline", attributes: editableCellAttributes },
    {
      id: "actions",
      sort: false,
      formatter: (cell, row) =>
        gridjs.html(
          `<button type="button" onclick="triggerDelete(${row.cells[0].data})">Delete</button>`
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
          "tour_program_id",
          "tour_program_name",
          "max_number_of_customer",
          "destination_city",
          "destination_country",
          "duration",
          "min_price",
          "max_price",
          "tour_detail",
          "airline",
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
