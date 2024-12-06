# Americansouth

Motivation: Monitor internet data usage to avoid unexpected overage charges from Astound.

## Usage

The tool processes data usage information from a JSON file in this format:

```json
[
  {
    "date": "2024-11-13",
    "amount": 79.13,
    "amountUnits": "GB",
    "total": 400,
    "totalUnits": "GB",
    "overage": 0,
    "overageUnits": "GB",
    "scrapedAt": "2024-11-13T06:17:28.611Z"
  },
  {
    "date": "2024-11-13",
    "amount": 79.13,
    "amountUnits": "GB",
    "total": 400,
    "totalUnits": "GB",
    "overage": 0,
    "overageUnits": "GB",
    "scrapedAt": "2024-11-13T06:41:24.588Z"
  }
]
```

Run the script by passing the JSON file:

```bash
americansouth data.json
```

Example output:

```
  DAILY USED DAILY BUDGET   TOTAL USED MONTHLY BUDGET      TOTAL DATA FETCH TIME
--------------------------------------------------------------------------------------------
        61GB         16GB         61GB          338GB      400GB Sat Nov 09 11:58 pm 2024
         5GB         17GB         66GB          333GB      400GB Mon Nov 11 07:49 am 2024
         5GB         17GB         71GB          328GB      400GB Mon Nov 11 09:12 pm 2024
         7GB         18GB         79GB          320GB      400GB Tue Nov 12 10:41 pm 2024
         6GB         18GB         85GB          314GB      400GB Wed Nov 13 08:07 pm 2024
         8GB         19GB         93GB          306GB      400GB Thu Nov 14 04:25 pm 2024
        14GB         19GB        107GB          292GB      400GB Fri Nov 15 08:17 am 2024
        12GB         20GB        120GB          279GB      400GB Sun Nov 17 07:59 am 2024
         7GB         22GB        127GB          272GB      400GB Mon Nov 18 07:52 am 2024
         5GB         23GB        133GB          266GB      400GB Tue Nov 19 07:37 am 2024
        14GB         22GB        147GB          252GB      400GB Tue Nov 19 01:43 pm 2024
```

The output shows:

- Daily data usage
- Recommended daily budget to stay within monthly limit
- Total data used so far
- Remaining monthly budget
- Total monthly allocation
- Timestamp of when data was fetched
