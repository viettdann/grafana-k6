export const options = {
    // define thresholds
    thresholds: {
      http_req_failed: ['rate<0.01'], // http errors should be less than 1%
      http_req_duration: ['p(99)<1000'], // 99% of requests should be below 1s
    },
    // define scenarios
    scenarios: {
      // arbitrary name of scenario
      average_load: {
        executor: 'ramping-vus',
        stages: [
          // ramp up to average load of 20 virtual users
          { duration: '10s', target: 20 },
          // maintain load
          { duration: '50s', target: 20 },
          // ramp down to zero
          { duration: '5s', target: 0 },
        ],
      },
    },
  };