# Online Shopping Monitor for Shopify Sites

### Functionality:
- The monitor will look for a specified product on a website and add it to cart when avaialble in specified size
- Will also fill out User's info like email, address, and payment
- The monitor will complete the order once all of the required fields are filled out

### Setup:
- Product information is stored in local JSON files in directory called "info"
- The two JSON files are named "user_info" and "product_info"
- Personal information is pulled from user_info" for user information like payment and personal info
- Product information like name and size are pulled from "product_info"
- The user must edit these JSON files for their own information in order to make successful purchases

### Sample JSON File Format:
- user_info.json:
{
	"personal":{
		"email": "example@gmail.com",
		"firstName": "Joe",
		"lastName": "Mama",
		"phone": "1234567891"
	},
	"address": {
		"street": "123 First St.",
		"address2": "Apt. A",
		"city": "San Francisco",
		"country": "United States",
		"state": "California",
		"zip": "94106"
	},
	
	"payment": {
		"name": "Joe Mama",
		"card1": "1234",
		"card2": "1234",
		"card3": "1234",
		"card4": "1234",
		"exMonth": "12",
		"exYear": "34",
		"vCode": "123"
	}

}


- product_info.json:
{
	"product_name": "ADIDAS YEEZY BOOST 380",
	"size": "9"
}
