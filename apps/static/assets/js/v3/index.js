function libb(inputString) {
    let formattedList = "";
    inputString.forEach((item) => {
      formattedList += `<li class="list-group-item">${item.trim()}</li>`;
    });
    return formattedList;
}
$(document).ready(function () {
    // Tombol clear input
    $('#clearButton').on('click', function () {
      $('#searchInput').val('').focus();
      $(this).hide();
    });

    // Tampilkan tombol clear saat ada input
    $('#searchInput').on('input', function () {
      if ($(this).val() !== '') {
        $('#clearButton').show();
      } else {
        $('#clearButton').hide();
      }
    });

    $('#searchButton').on('click', function () {
      const query = $("#searchInput").val();
      const loweredQuery = query.toLowerCase();
      // set tipe
      $('#submitEvaluasi').data('tipe', '0');
      $.ajax({
        url: api_url+"/cari/" + loweredQuery,
        type: "get",
        dataType: "json",
        beforeSend: function () {
          $('.loading').fadeIn();
        },
        success: function (results) {
          console.log(results);
          setTimeout(function () {
            $('.loading').fadeOut();
            hasil(results)
          }, 800);
        },
      });
    });
    $('#searchSemantik').on('click', function () {
      const query = $("#searchInput").val();
      const loweredQuery = query.toLowerCase();
      if(query == ''){
        swal.fire({
            title: "Gagal melakukan pencarian",
            html: "Query Belum dimasukkan",
            icon: "warning"
        });
        return;
      }
      // set tipe
      $('#submitEvaluasi').data('tipe', '1');
      $.ajax({
        url: api_url+"/semantik/" + loweredQuery,
        type: "get",
        dataType: "json",
        beforeSend: function () {
          $('.loading').fadeIn();
        },
        success: function (results) {
          console.log(results);
          setTimeout(function () {
            $('.loading').fadeOut();
            hasil(results)
          }, 800);
        },
        error: function(e) {
            $('.loading').fadeOut();
            swal.fire({
                title: "Gagal melakukan pencarian",
                html: e.responseJSON.error,
                icon: "warning"
            });
        }
      });
    });
  });
function hasil(results){
    // Render hasil pencarian
    const $resultContainer = $('.search-result');
    $resultContainer.empty();
    results.data.forEach(result => {
      const resultHtml = `
        <div class="result-item">
          <div class="d-flex justify-content-between align-items-center">
            <span>${result.quran_format} (${result.surah + ' - '+ result.nama_latin })</span>
            <input type="checkbox" class="result-checkbox">
          </div>
          <div class="result-detail">
            <p class="card-text text-right fs-4">${result.isi_ayat}</p>
            <p class="card-text text-justify">${result.ayat_indo}</p>
            <p class="card-text text-justify">${libb(result.breadcrumb)}</p>
          </div>
        </div>
      `;
      $resultContainer.append(resultHtml);
    });
    $(document).on('click', '.result-item', function (e) {
        // Cek jika target klik adalah checkbox, jika ya, tidak melakukan apapun
        if ($(e.target).is('.result-checkbox')) {
            return;
        }
    
        const $detail = $(this).find('.result-detail');
        
        // Periksa jika detail sudah terlihat, jika ya, maka slide up, jika tidak, maka slide down
        if ($detail.is(":visible")) {
            $detail.slideUp();
        } else {
            $detail.slideDown();
        }
    });
    // Tampilkan hasil pencarian
    $resultContainer.fadeIn();
}
// Evaluasi hasil pencarian
$("#submitEvaluasi").click(function() {
    const query = $("#searchInput").val();
    if(query == ''){
        swal.fire({
            title: "Gagal melakukan Evaluasi",
            html: "Query Belum dimasukkan",
            icon: "warning"
        });
        return;
    }
    const tipe = $(this).data('tipe')
    let relevance = [];
    $(".result-checkbox").each(function() {
        relevance.push($(this).is(":checked") ? 1 : 0);
    });

    // Hitung metrik evaluasi di JavaScript
    const precision = calculatePrecision(relevance);
    const recall = calculateRecall(relevance);
    const f1Score = calculateF1Score(precision, recall);
    const map = calculateMAP(relevance);
    const ndcg = calculateNDCG(relevance);

    // Kirim hasil evaluasi ke server
    $.ajax({
        url: api_url+"evaluasi",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ 
            query: query,
            tipe: tipe,
            relevance: relevance,
            metrics: { precision, recall, f1Score, map, ndcg }
        }),
        success: function(response) {
            alert("Evaluasi berhasil disimpan!");
        },
        error: function() {
            alert("Gagal menyimpan evaluasi. Silakan coba lagi.");
        }
    });
});