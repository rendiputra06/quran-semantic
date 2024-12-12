function beforeSend() {
    let startTime = new Date().getTime(); // Waktu awal saat tampilan swal dibuka

    // Update stopwatch setiap 1000 milidetik (1 detik)
    const intervalId = setInterval(() => {
        const currentTime = new Date().getTime();
        const elapsedTime = (currentTime - startTime) / 1000; // Menghitung waktu dalam detik
        const formattedTime = formatStopwatchTime(elapsedTime);

        // Update pesan HTML dengan stopwatch yang terus berjalan
        swal.update({
            html: `Memproses data<br>Waktu: ${formattedTime}`
        });
    }, 1000);

    // Menampilkan swal.fire dengan pesan awal
    swal.fire({
        title: 'Menunggu',
        html: 'Memproses data<br>Waktu: 0:00',
        didOpen: () => { swal.showLoading() },
        allowOutsideClick: false,
        willClose: () => {
            clearInterval(intervalId); // Menghentikan interval saat swal ditutup
        }
    });
}

// Fungsi untuk memformat waktu dalam format menit:detik
function formatStopwatchTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}

var totalResults = 0;
// Display search results
function displaySearchResults(results, jumlah) {
    const resultsContainer = $('#searchResults');
    resultsContainer.empty();

    totalResults = jumlah
    $('#jml').text(jumlah)

    results.forEach(result => {
        resultsContainer.append(`<div class="card mb-2">
            <div class="card-body">
                <h5 class="card-title text-right">${result.surah + ' - '+ result.nama_latin }</h5>
                <p class="card-text text-right">${result.isi_ayat}</p>
                <p class="card-text text-justify">${result.ayat_indo}</p>
                <p class="card-text">(${result.surah}) | (${result.nomor_di_surah}) | (${result.nomor_ayat})</p>
                <div class="form-check">
                    <input type="checkbox" class="form-check-input" data-ayah="${result.nomor_ayat}">
                    <label class="form-check-label">Hasil ini Relevan</label>
                </div>
            </div>
        </div>`);
    });
}

function convertToQuranFormat(inputString) {
    // Memisahkan nomor surat dan nomor ayat dari inputString
    const surahNumber = parseInt(inputString.substring(1, 4), 10);
    const ayahNumber = parseInt(inputString.substring(5), 10);

    // Membuat format "QS. x:y" dari nomor surat dan nomor ayat
    const result = `QS. ${surahNumber}:${ayahNumber}`;

    return result;
}

function tampilkan(ayat, jumlah)
{
    const tablenya = $('#tdhasil');
    tablenya.empty();
    totalResults = jumlah
    $('#tdjumlah').text(jumlah)
    // Populate the table with search results
    ayat.forEach(result => {
        const row = $(`<li>${convertToQuranFormat(result.nomor_ayat)}</li>`);
        tablenya.append(row);
    });
    console.log('ini jalan kok');

}

function searchWord(query) {
    const loweredQuery = query.toLowerCase();
    // const filteredResults = searchResults.filter(result => result.text.toLowerCase().includes(loweredQuery));
    $.ajax({
        url: api_url+'/cari/'+loweredQuery,
        type: 'get',
        dataType: 'json',
        beforeSend: function() {
            swal.fire({
                title: "Menunggu",
                html: "Memproses data",
                didOpen: () => {
                  swal.showLoading();
                },
              });
        },
        success: function (result) {
            console.log(result);
            setTimeout(function() {
                displaySearchResults(result.data, result.length);
                // renderProductList(['......'])
                $('#productList').html('........')
                tampilkan(result.data, result.length)
                swal.close()
            }, 800);
        }
    });
}
function searchSinonim(query) {
    const loweredQuery = query.toLowerCase();
    // const filteredResults = searchResults.filter(result => result.text.toLowerCase().includes(loweredQuery));
    $.ajax({
        url: api_url+'/semantic/similar-verse-sinonim/'+loweredQuery,
        type: 'get',
        dataType: 'json',
        beforeSend: function() {
            swal.fire({
                title: "Menunggu",
                html: "Memproses data",
                didOpen: () => {
                  swal.showLoading();
                },
              });
        },
        success: function (result) {
            console.log(result);
            setTimeout(function() {
                displaySearchResults(result.data, result.length);
                renderProductList(result.kata)
                swal.close()
            }, 800);
        }
    });
}
function searchSemantik(query) {
    const loweredQuery = query.toLowerCase();
    // const filteredResults = searchResults.filter(result => result.text.toLowerCase().includes(loweredQuery));
    $.ajax({
        url: api_url+'/semantik/'+loweredQuery,
        type: 'get',
        dataType: 'json',
        beforeSend: function() {
            swal.fire({
                title: "Menunggu",
                html: "Memproses data",
                didOpen: () => {
                  swal.showLoading();
                },
              });
        },
        success: function (result) {
            console.log(result);
            setTimeout(function() {
                displaySearchResults(result.data, result.length);
                renderProductList(result.kata)
                tampilkan(result.data, result.length)
                swal.close()
            }, 800);
        }
    });
}

// Function to render the product list dynamically
function renderProductList(products) {
    var productListElement = $('#productList');
    
    // Clear existing items
    productListElement.empty();
  
    // Add each product dynamically
    products.forEach(function(productName) {
      var listItem = $('<li class="list-group-item d-flex justify-content-between lh-condensed"></li>');
      listItem.append('<p class="my-0">' + productName.word + ' / ' + scoreResult(productName.score) +'</p>');
      productListElement.append(listItem);
    });
}
function scoreResult(score)
{
    // Menggunakan toFixed untuk membatasi angka desimal menjadi 3 digit
    const shortenedNumber = Number(score.toFixed(3));

    return shortenedNumber;
}

   // Event listener for checkbox
$('#searchResults').on('change', 'input[type=checkbox]', function () {
    // Update MAP on each checkbox change
    calculateAndDisplayMAP();
});

function hitungMAP(){

}
// Function to calculate and display real-time MAP
function calculateAndDisplayMAP() {
    const checkboxes = $('#searchResults input[type=checkbox]');
    const totalRelevant = checkboxes.length;

    console.log('Total hasil yang dipilih = ' + totalRelevant)
    let precisionSum = 0.0;
    let relevantCount = 0;
    let apCount = 0;

    checkboxes.each(function (index) {
        const checkbox = $(this);
        const isChecked = checkbox.prop('checked'); // atau bisa juga menggunakan checkbox.is(':checked')
        
        if (isChecked) {
            relevantCount++;
            precisionSum = relevantCount / (index + 1);
            apCount += precisionSum
        }else{
            precisionSum = relevantCount / (index + 1);
        }
        console.log('posisi = ', index + 1, ', tercentang = ', isChecked);
        console.log('precisionSum = ', precisionSum);
        console.log('apCount = ', apCount);
    });
    
    const realTimeMAP = totalRelevant > 0 ? apCount / relevantCount : 0.0;

    // Display real-time MAP
    $('#realTimeMap').text(realTimeMAP.toFixed(4));
}

// Event listener for search query input
$('.runSearch').on('click', function () {
    var jenis = $(this).data('id');

    const query = $('#searchQuery').val();

    // Validasi query tidak boleh kosong atau null
    if (!query) {
        // Tampilkan pesan error atau ambil tindakan yang sesuai
        console.error('Query cannot be empty');
        return;
    }

    switch (jenis) {
        case 1:
            searchWord(query)
            break;
        case 2:
            searchSinonim(query)
            break;
        case 3:
            searchSemantik(query)
            break;
    
        default:
            break;
    }
    // hitung MAP ketika sudah berhasil melakukan pencarian
    calculateAndDisplayMAP()
    $('#submitRating').attr('disabled', false)
});

$('#copy').on('click', function(){
    hasil = $('#tdhasil').html();
    console.log(hasil);
})