function signout() {
  Cookies.remove('hcp_realstate');
  window.location.href = "/auction/login";
}

    // Function to show the modal
    function showPleaseWait() {
      $('#pleaseWaitModal').modal('show');
    }
  
    // Function to hide the modal
    function hidePleaseWait() {
      $('#pleaseWaitModal').modal('hide');
    }
  
  
function checkLogin() {
  if (Cookies.get('hcp_realstate') == null) {
    window.location.href = "/auction/login";
  }
}

function viewAll() {
  $.ajax({
    type: "POST",
    url: "view_page/",
    success: function (result) {
      var summary_data = [];
      var data = result["data"];

      for (let x = 0; x < data.length; x++) {
        let address = data[x]['address'].replace(/\s+/g, '+');
        let address2 = data[x]['address'].replace(/\s+/g, '-');
        let parcel = data[x]['parcel_id'];

        summary_data.push({
          'Date': data[x]['date'],
          'Auction Status': data[x]['auction_status'],
          'Auction Type': data[x]['auction_type'],
          'AI Assistance':'<a href="javascript:void(0);"  onclick="javascript:auditWithAI(\'' + data[x]['case_number'] + '\');">Audit using AI</a>',

          'Case Number': data[x]['case_number'],
          'Final Judgement': data[x]['final_judgement'],
          'Appraiser': `<a href="http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID=${parcel}" target="_blank">${data[x]['parcel_id']}</a>`,
          'Zillow View': `<a href="https://www.zillow.com/homes/${address2}" target="_blank">${data[x]['address']}</a>`,
          'Google View': `<a href="https://www.google.com/maps/place/${address}" target="_blank">View</a>`,
          'Taxes': `<a href="https://hillsborough.county-taxes.com/public/search/property_tax?search_query=${address}" target="_blank">View</a>`,

          'Assessed Value': data[x]['assessed_value'],
          'Max Bid': data[x]['max_bid'],
          'Is Watching': data[x]['is_watching'] +
            '</br><span class="link" onclick="javascript:follow_case(\'' + data[x]['case_number'] + '\');">Follow</span>' +
            '</br><span class="link" onclick="javascript:stop_following(\'' + data[x]['case_number'] + '\');">Un-follow</span>',
          'Is Sold': data[x]['is_house_sold'],
          'Is Canceled': data[x]['is_canceled'],
          
        });
      }

      if (summary_data.length > 0) {
        $('#intel_table').DataTable({
          responsive: true,
          fixedHeader: true,
          paging: true,
          sort: true,
          retrieve: true,
          destroy: true,
          pageLength: 5,
          data: summary_data,
          columns: [
            { data: "Date" },
            { data: "Auction Status" },
            { data: "Auction Type" },
            { data: "AI Assistance" },

            { data: "Case Number" },
            { data: "Final Judgement" },
            { data: "Appraiser" },
            { data: "Zillow View" },
            { data: "Google View" },
            { data: "Taxes" },

            { data: "Assessed Value" },
            { data: "Max Bid" },
            { data: "Is Watching" },
            { data: "Is Sold" },
            { data: "Is Canceled" },
          ]
        });
      }
    },
    error: function (result) {
      console.debug(result);
    }
  });
}

function filter(search) {
  $.ajax({
    type: "POST",
    url: "filter_data/",
    data: {
      filter: search,
      crsfmiddlewaretoken: '{{ csrf_token }}'
    },
    success: function (result) {
      var summary_data = [];
      var data = result["data"];

      for (let x = 0; x < data.length; x++) {
        let address = data[x]['address'].replace(/\s+/g, '+');
        let address2 = data[x]['address'].replace(/\s+/g, '-');
        let parcel = data[x]['parcel_id'];

        summary_data.push({
          'Date': data[x]['date'],
          'Auction Status': data[x]['auction_status'],
          'Auction Type': data[x]['auction_type'],
          'AI Assistance':'<a href="javascript:void(0);"  onclick="javascript:auditWithAI(\'' + data[x]['case_number'] + '\');">Audit using AI</a>',

          'Case Number': data[x]['case_number'],
          'Final Judgement': data[x]['final_judgement'],
          'Appraiser': `<a href="http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID=${parcel}" target="_blank">${data[x]['parcel_id']}</a>`,
          'Zillow View': `<a href="https://www.zillow.com/homes/${address2}" target="_blank">${data[x]['address']}</a>`,
          'Google View': `<a href="https://www.google.com/maps/place/${address}" target="_blank">View</a>`,
          'Taxes': `<a href="https://hillsborough.county-taxes.com/public/search/property_tax?search_query=${address}" target="_blank">View</a>`,

          'Assessed Value': data[x]['assessed_value'],
          'Max Bid': data[x]['max_bid'],
          'Is Watching': data[x]['is_my_watchlist'] +
            '</br><a href="javascript:void(0);" onclick="follow_case(\'' + data[x]['case_number'] + '\');">Follow</a>' +
            '</br><a href="javascript:void(0);" onclick="stop_following(\'' + data[x]['case_number'] + '\');">Un-follow</a>',
          'Is Sold': data[x]['is_house_sold'],
          'Is Canceled': data[x]['is_canceled'],

          
        });
      }

      if (summary_data.length > 0) {
        $('#intel_table').empty();
        $('#intel_table').DataTable().destroy();

        $('#intel_table').DataTable({
          responsive: true,
          fixedHeader: true,
          paging: true,
          sort: true,
          retrieve: true,
          pageLength: 5,
          data: summary_data,
          columns: [
            { data: "Date" },
            { data: "Auction Status" },
            { data: "Auction Type" },
            { data: "AI Assistance" },

            { data: "Case Number" },
            { data: "Final Judgement" },
            { data: "Appraiser" },
            { data: "Zillow View" },
            { data: "Google View" },
            { data: "Taxes" },
            { data: "Assessed Value" },
            { data: "Max Bid" },
            { data: "Is Watching" },
            { data: "Is Sold" },
            { data: "Is Canceled" },
           
          ]
        });
      } else {
        $('#intel_table').empty();
      }
    },
    error: function (result) {
      console.debug(result);
    }
  });
}

function follow_case(case_number) {
  $.ajax({
    type: "POST",
    url: "follow/",
    data: {
      case: case_number,
      crsfmiddlewaretoken: '{{ csrf_token }}'
    },
    success: function () {},
    error: function (result) {
      alert("Error saving event");
      console.debug(result);
    }
  });
}

function stop_following(case_number) {
  $.ajax({
    type: "POST",
    url: "unfollow/",
    data: {
      case: case_number,
      crsfmiddlewaretoken: '{{ csrf_token }}'
    },
    success: function () {},
    error: function (result) {
      alert("Error saving event");
      console.debug(result);
    }
  });
}

$(document).ready(function () {
  checkLogin();
  viewAll();
});
