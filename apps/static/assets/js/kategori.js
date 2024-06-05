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
                let roww = `<li class="list-group-item mr-1 ml-1 hover">
                        <input type="radio" name="radio-group" class="form-check-input" value="${record[0]}" id="exampleCheck${record[0]}">
                        <a href="#" class="font-weight-bold" data-id="${record[0]}">${record[1]}</a>
                    </li>`;
                main.append(roww);
            });
        }
    });
}

function load_subcategories(parentId, container, parent_name) {
    // Hapus semua subkategori yang ada
    let level = container.data('level');
    if(level == 1){
        $('.col-sm-3').not(container).remove();
    }else{
        $('.col-sm-3').each(function() {
            if ($(this).data('level') > level) {
                $(this).remove();
            }
        });
    }
    
    $.ajax({
        url: '/view_subkategori/',
        method: 'GET',
        data: { parent_id: parentId },
        success: function(response) {
            const subUl = $('<ul class="list-group list-group-flush kategoris"></ul>');
            if(response.ayat){
                response.records.forEach(function(record) {
                    let subLi = `<li class="list-group-item mr-1 ml-1 hover">
                            <a href="#" class="font-weight-bold" data-id="${record}" data-ayat="1">${record}</a>
                        </li>`;
                    subUl.append(subLi);
                });
            }else{
                response.records.forEach(function(record) {
                    let subLi = `<li class="list-group-item mr-1 ml-1 hover">
                        <input type="radio" name="radio-group" class="form-check-input" value="${record[0]}" id="exampleCheck${record[0]}">
                            <a href="#" class="font-weight-bold" data-id="${record[0]}" data-ayat="0">${record[1]}</a>
                        </li>`;
                    subUl.append(subLi);
                });
            }
            let addSubLi = `<li class="list-group-item mr-1 ml-1 hover">
                <button class="btn btn-primary btn-sm tambah-sub" data-parent="${parentId}">Tambah</button>
            </li>`;
            subUl.append(addSubLi);

            const newCard = `
                <div class="card">
                    <div class="card-header">
                        <h5>${parent_name}</h5>
                    </div>
                        ${subUl.prop('outerHTML')}
                </div>`;

            const newCol = $('<div class="col-sm-3" data-level="'+(parseInt(level) + 1) +'"></div>').append(newCard);
            container.after(newCol);
        }
    });
}
$('#addCategory').on('click', function(e) {
    $('#addForm').trigger('submit')
});
$('#load_data').on('click', function(e) {
    load_data()
});


$('#clearSubcategoriesBtn').on('click', function() {
    clearSubcategories();
});

function clearSubcategories() {
    $('.col-sm-3').not(':first').remove();
}

function tampilkanAyat(value)
{
    $.ajax({
        url: '/view_ayat/',
        method: 'GET',
        data: { value: value },
        beforeSend: function(){
            swal.fire({title: 'Menunggu',html: 'Memproses data',didOpen: () => {swal.showLoading()}})
        },
        success: function(response) {
            console.log(response)
            // Memeriksa apakah response berisi data
            if (response.records && response.records.length > 0) {
                var ayatContent = '';
                
                // Menggabungkan semua ayat dalam response menjadi satu string
                response.records.forEach(function(result) {
                    // ayatContent += '<h4>' + ayat.isi_ayat + '</h4>';
                    // ayatContent += '<p>' + ayat.ayat_indo + '</p>';
                    ayatContent += `<div class="card mb-2">
                        <div class="card-body">
                            <h3 class="card-title text-right">${result.surah_nama + ' ~ ' + result.surah_nama_latin}</h3>
                            <h4 class="card-text text-right">${result.isi_ayat}</h4>
                            <p class="card-text text-justify">${result.ayat_indo}</p>
                            <p class="card-text">(${result.surah_nama + ' ~ ' + result.surah_nama_latin}) | (${result.nomor_di_surah}) | (${result.nomor_ayat})</p>
                        </div>
                    </div>`;
                });
                
                // Menampilkan ayat dalam modal
                $('#tampilModal').find('.modal-body').html(ayatContent);
            } else {
                $('#tampilModal').find('.modal-body').html('<p>Ayat tidak ditemukan.</p>');
            }
            setTimeout(function() {
                swal.close()
                $('#tampilModal').modal('show');
            }, 800);
        }
    });
}