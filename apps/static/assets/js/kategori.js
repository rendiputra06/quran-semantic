function load_data()
{
    console.log('load_data')
    $.ajax({
        url: '/view_kategori/',
        method: 'GET',
        success: function(response) {
            const main = $('#main-ul');
            main.empty();
            response.records.forEach(function(record) {
                let roww = `<li class="list-group-item list-group-item-action hover" data-id="${record[0]}">
                        <a href="#" class="font-weight-bold">${record[1]}</a>  
                        <button type="button" class="btn btn-sm btn-outline-primary dropdown-toggle" data-toggle="dropdown">
                            <i class="fas fa-ellipsis-h"></i> 
                        </button>
                        <div class="dropdown-menu dropdown-menu-right">
                            <button class="dropdown-item editBtn" data-id="${record[0]}">Edit</button>
                            <button class="dropdown-item deleteBtn" data-id="${record[0]}">Hapus</button>
                        </div>
                    </li>`;
                main.append(roww);
            });

            // Attach event handlers to dynamically created buttons
            attachEventHandlers();
        }
    });
}

function load_subcategories(parentId, container) {
    $.ajax({
        url: '/view_subkategori/',
        method: 'GET',
        data: { parent_id: parentId },
        success: function(response) {
            const subUl = $('<ul class="list-group list-group-flush"></ul>');
            response.records.forEach(function(record) {
                let subLi = `<li class="list-group-item list-group-item-action hover" data-id="${record[0]}">
                        <a href="#" class="font-weight-bold">${record[1]}</a>  
                        <button type="button" class="btn btn-sm btn-outline-primary dropdown-toggle" data-toggle="dropdown">
                            <i class="fas fa-ellipsis-h"></i> 
                        </button>
                        <div class="dropdown-menu dropdown-menu-right">
                            <button class="dropdown-item editBtn" data-id="${record[0]}">Edit</button>
                            <button class="dropdown-item deleteBtn" data-id="${record[0]}">Hapus</button>
                        </div>
                    </li>`;
                subUl.append(subLi);
            });

            const parentName = container.find('a.font-weight-bold').text();
            const newCard = `
                <div class="card">
                    <div class="card-header">
                        <h5>${parentName}</h5>
                    </div>
                    <div class="card-body">
                        ${subUl.prop('outerHTML')}
                    </div>
                </div>`;

            const newCol = $('<div class="col-sm-3"></div>').append(newCard);
            container.after(newCol);

            // Attach event handlers to dynamically created buttons
            attachEventHandlers();
        }
    });
}

$('#addForm').on('submit', function(e) {
    e.preventDefault();
    const formData = $('#addForm').serialize();
    $.ajax({
        url: '/add_kategori/',
        method: 'POST',
        data: formData,
        success: function(response) {
            // alert(response.msg);
            $('#load_data').click();
            $('#addForm')[0].reset();
            $('#exampleModal').modal('hide');
        }
    });
});
$('#addCategory').on('click', function(e) {
    $('#addForm').trigger('submit')
});
$('#load_data').on('click', function(e) {
    load_data()
});
function attachEventHandlers() {
    // Edit Student
    $('.editBtn').on('click', function() {
        $.ajax({
            url: '/edit_kategori/',
            method: 'GET',
            data: { id: $(this).data('id') },
            success: function(response) {
                console.log(response)
                record = response.records
                $('#addForm input[name="id"]').val(record[0]);
                $('#addForm input[name="mode"]').val('update');
                $('#addForm input[name="name"]').val(record[1]);
                $('#addForm input[name="parent_id"]').val(record[2]);
                $('#exampleModal').modal('show');
            }
        });
    });

    // Delete Student
    $('.deleteBtn').on('click', function() {
        const studentId = $(this).data('id');
        if (confirm('Are you sure you want to delete this record?')) {
            $.ajax({
                url: '/delete_kategori/',
                method: 'POST',
                data: { id: studentId },
                success: function(response) {
                    alert(response.msg);
                    $('#load_data').click();
                }
            });
        }
    });
}

$(document).ready(function() {
    load_data();

    $('#main-ul').on('click', 'li', function() {
        const parentId = $(this).data('id');
        const container = $(this).closest('.col-sm-3');
        load_subcategories(parentId, container);
    });
});