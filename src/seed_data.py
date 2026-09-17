CUSTOMERS={
"SK4821X":{"name":"Priya Nair","tier":"Gold","contact":"priya.nair@example.com / +91-98xxxxxxx1","history":"6 flights; 1 prior complaint (delayed baggage, resolved with voucher)","segments":[{"flight":"SK-204","route":"Delhi → Goa","date":"Wed 23 Sep 2026","scheduled":"18:40","status":"Cancelled (operational reasons)","delay":0},{"flight":"Return","route":"Goa → Delhi","date":"Fri 25 Sep 2026","scheduled":"16:20","status":"Unaffected","delay":0}]},
"TR1190B":{"name":"Arvind Kulkarni","tier":"Silver","contact":"arvind.kulkarni@example.com / +91-98xxxxxxx2","history":"3 flights; no prior complaints","segments":[{"flight":"SK-118","route":"Mumbai → Bengaluru","date":"Wed 23 Sep 2026","scheduled":"07:10","new":"11:10","status":"Delayed 4h","delay":4}]},
"WL7742":{"name":"Meher Kaur","tier":"Platinum","contact":"meher.kaur@example.com / +91-98xxxxxxx3","history":"10 flights; 1 prior complaint (overbooking, resolved with tier-status upgrade)","segments":[{"flight":"SK-305","route":"Delhi → Hyderabad","date":"Wed 23 Sep 2026","scheduled":"14:00","new":"20:00","status":"Delayed 6h","delay":6}]}}
POLICIES={
"CANCEL":"Airline cancellation: free rebooking on the next available flight within 24 hours, or a full refund, customer's choice.",
"DELAY_LT3":"Delay under 3 hours: ₹500 meal voucher.","DELAY_GT3":"Delay more than 3 hours: meal voucher + lounge access.",
"DELAY_GT5":"Delay more than 5 hours: meal voucher + hotel accommodation covering only delayed hours, not a full night's stay.",
"REFUND":"Airline-caused cancellation refunds are full, within 7 business days, to original payment method only.",
"FARE":"Voluntary higher-fare rebooking requires paying the difference; agents cannot waive above ₹1,500 without supervisor approval.",
"LOYALTY":"Gold and Platinum get priority rebooking, but no additional compensation.",
"ESCALATE":"Beyond-policy compensation, waiver above ₹1,500, non-airline exception, legal threat/formal complaint, or different-method refund must escalate."}
SCENARIOS={"SK4821X":"I'm furious. I want a full cash refund and a free business-class upgrade on my return for the trouble.","TR1190B":"This 4-hour delay will make me miss a meeting. I want a hotel.","WL7742":"I want a full night's hotel and a higher-fare flight instead. Please waive the ₹2,000 difference."}
