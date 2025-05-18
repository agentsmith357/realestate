

function signout() {
    Cookies.remove('hcp_realstate');
    window.location.href = "/auction/login";
  }

  function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value;
    if (!message) return;

    const chatMessages = document.getElementById('chatMessages');
    const userMsg = document.createElement('div');
    userMsg.textContent = `You: ${message}`;
    chatMessages.appendChild(userMsg);

    input.value = '';

    // Dummy AI reply
    const botMsg = document.createElement('div');
    botMsg.textContent = 'AI: Let me look into that...';
    chatMessages.appendChild(botMsg);

    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // viewAll() and filter() should go here

  function checkLogin(){
      // Read the cookie
      if (Cookies.get('hcp_realstate') == null)
      {
        window.location.href = "/auction/login";


      }
     }

    function viewAll()
    {
      $.ajax({
        type: "POST",
        url: "view_page/",
        success: function(result)
        {
          var summary_data = []
          var data = result["data"];

     

          for(x=0;x< data.length;x++)
          {
            // ref="http://www.omsaicreche.blogspot.com" onclick="location.href='http://www.omsaivatikanoida.blogspot.com';" target="_blank"
            // https://www.zillow.com/homes/10503-marsanne-place,%20riverview-fl/
            //  'Open Javascript':'<span class="link" onclick="javascript:get_data(\''+data[x]['date']+'\');">'+data[x]['date'] + '</span>'
            //https://www.google.com/maps/place/10503+Marsanne+Pl,+Riverview,+FL+33578/
            //http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID=1928059AG000015000020U
            address = data[x]['address'].replace(/\s+/g,'+');
            address2 = data[x]['address'].replace(/\s+/g,'-');
            parcel = data[x]['parcel_id']

            var google_string = "https://www.google.com/maps/place/"+address
            var zillow_string = "https://www.zillow.com/homes/"+address2              
            var appraiser_string = "http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID="+parcel
            var tax_string = "https://hillsborough.county-taxes.com/public/search/property_tax?search_query="+address

            summary_data.push({
            'Date':data[x]['date'],
            'Auction Status':data[x]['auction_status'],
            'Auction Type':data[x]['auction_type'],
            'Case Number':data[x]['case_number'],
            'Final Judgement':data[x]['final_judgement'],
            'Appraiser':'<a href='+appraiser_string+' target="_blank">'+data[x]['parcel_id']+'</a>',
            'Zillow View':'<a href='+zillow_string+' target="_blank">'+data[x]['address']+'</a>',
            'Google View':'<a href='+google_string+' target="_blank">View</a>',
            'Taxes':'<a href='+tax_string+' target="_blank">View</a>',
            'Assessed Value':data[x]['assessed_value'],
            'Max Bid':data[x]['max_bid'],
            'Is Watching':data[x]['is_watching'] +'</br><span class="link" onclick="javascript:follow_case(\''+data[x]['case_number']+'\');">Follow</span></br> <span class="link" onclick="javascript:stop_following(\''+data[x]['case_number']+'\');">Un-follow</span>',
            'Is Sold':data[x]['is_house_sold'],
            'Is Canceled':data[x]['is_canceled'],
          
          });
          }
          //http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID=1928059AG000015000020U
          //https://pubrec6.hillsclerk.com/PAVDirectSearch/index.html?CQID=320&OBKey__1006_1=2023287596
          if (summary_data.length > 0)
          {

            var intel_table = $('#intel_table');
              
            intel_table.DataTable({
              responsive: true,
              fixedHeader: true,
              paging: true,
              sort: true,
              retrieve: true,
              pageLength: 5,
              rowReorder: {
                selector: 'td:nth-child(2)'
            },
              "data": summary_data,
              "columns":[
              { "data" :"Date" },
              { "data" :"Auction Status" },
              { "data" :"Auction Type" },
              { "data" :"Case Number" },
              { "data" :"Final Judgement" },
              { "data" :"Appraiser" },
              { "data" :"Zillow View" },
              { "data" :"Google View" },
              { "data" :"Taxes" },
              { "data" :"Assessed Value" },
              { "data" :"Max Bid" },
              { "data" :"Is Watching" },
              { "data" :"Is Sold" },
              { "data" :"Is Canceled" },
              ]
            
            });

      

        
          }
          else{
          
          }
        },
        error:function(result)
        {
          console.debug(result);

        }
      });
    }


    function filter(search)
    {
      $.ajax({
        type: "POST",
        url: "filter_data/",
        data: {"filter":search,
        crsfmiddlewaretoken: '{{ csrf_token }}'},
        success: function(result)
        {
          var summary_data = []
          var data = result["data"];


          for(x=0;x< data.length;x++)
          {
            // ref="http://www.omsaicreche.blogspot.com" onclick="location.href='http://www.omsaivatikanoida.blogspot.com';" target="_blank"
            // https://www.zillow.com/homes/10503-marsanne-place,%20riverview-fl/
            //  'Open Javascript':'<span class="link" onclick="javascript:get_data(\''+data[x]['date']+'\');">'+data[x]['date'] + '</span>'
            //https://www.google.com/maps/place/10503+Marsanne+Pl,+Riverview,+FL+33578/
            //http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID=1928059AG000015000020U

            //https://hillsborough.county-taxes.com/public/search/property_tax
            //https://hillsborough.county-taxes.com/public/search/property_tax?search_query=10503%20marsanne%20place&redirect=A0760207268
            //https://www.truthfinder.com/dashboard/reports/fl:brandon:33511:604sanfieldst
            address = data[x]['address'].replace(/\s+/g,'+');
            address2 = data[x]['address'].replace(/\s+/g,'-');
            parcel = data[x]['parcel_id']

            var google_string = "https://www.google.com/maps/place/"+address
            var zillow_string = "https://www.zillow.com/homes/"+address2              
            var appraiser_string = "http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID="+parcel
            var tax_string = "https://hillsborough.county-taxes.com/public/search/property_tax?search_query="+address
            summary_data.push({
            'Date':data[x]['date'],
            'Auction Status':data[x]['auction_status'],
            'Auction Type':data[x]['auction_type'],
            'Case Number':data[x]['case_number'],
            'Final Judgement':data[x]['final_judgement'],
            'Appraiser':'<a href='+appraiser_string+' target="_blank">'+data[x]['parcel_id']+'</a>',
            'Zillow View':'<a href='+zillow_string+' target="_blank">'+data[x]['address']+'</a>',
            'Google View':'<a href='+google_string+' target="_blank">View</a>',
            'Taxes':'<a href='+tax_string+' target="_blank">View</a>',
            'Assessed Value':data[x]['assessed_value'],
            'Max Bid':data[x]['max_bid'],
            'Is Watching':data[x]['is_my_watchlist'] +'</br><a href="javascript:void(0);" onclick="javascript:follow_case(\''+data[x]['case_number']+'\');">Follow</a></br> <a  href="javascript:void(0);" onclick="javascript:stop_following(\''+data[x]['case_number']+'\');">Un-follow</a>',
            'Is Sold':data[x]['is_house_sold'],
            'Is Canceled':data[x]['is_canceled'],
          
          });
          }
          //http://www.hcpafl.org/CamaDisplay.aspx?OutputMode=Display&SearchType=RealEstate&ParcelID=1928059AG000015000020U
          //https://pubrec6.hillsclerk.com/PAVDirectSearch/index.html?CQID=320&OBKey__1006_1=2023287596
          if (summary_data.length > 0)
          {
              $('#intel_table').empty();
              $('#intel_table').DataTable().destroy();
              var intel_table = $('#intel_table');
              
              intel_table.DataTable({
                responsive: true,
                fixedHeader: true,
                paging: true,
                sort: true,
                retrieve: true,
                pageLength: 5,
                rowReorder: {
                  selector: 'td:nth-child(2)'
              },
                "data": summary_data,
                "columns":[
                { "data" :"Date" },
                { "data" :"Auction Status" },
                { "data" :"Auction Type" },
                { "data" :"Case Number" },
                { "data" :"Final Judgement" },
                { "data" :"Appraiser" },
                { "data" :"Zillow View" },
                { "data" :"Google View" },
                { "data" :"Taxes" },
                { "data" :"Assessed Value" },
                { "data" :"Max Bid" },
                { "data" :"Is Watching" },
                { "data" :"Is Sold" },
                { "data" :"Is Canceled" },
                ]
              
              });              }
          else{
            $('#intel_table').empty();
          }
        },
        error:function(result)
        {
          console.debug(result);

        }
      });
    }

 function follow_case(case_number)
  {
    $.ajax({
      type: "POST",
      url: "follow/",
      data: {"case":case_number,
      crsfmiddlewaretoken: '{{ csrf_token }}'},
      success: function(result)
      {
        var summary_data = []
        //var data = result["data"];
        //filter('watching');

      },
      error:function(result)
      {
        alert("Error saving event");
        console.debug(result);

      }
    });
  }


  function stop_following(case_number)
  {
    $.ajax({
      type: "POST",
      url: "unfollow/",
      data: {"case":case_number,
      crsfmiddlewaretoken: '{{ csrf_token }}'},
      success: function(result)
      {
        var summary_data = []
        //var data = result["data"];
       // filter('watching');
      },
      error:function(result)
      {
        alert("Error saving event")
        console.debug(result);

      }
    });
  }

  $(document).ready(function () {
    checkLogin();
    viewAll();
  });