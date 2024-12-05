import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', function () {
  before(() => {
    queue.testMode = true;
  });

  afterEach(() => {
    queue.testMode = false;
    queue.shutdown(() => {});
  });

  it('should display an error message if jobs is not an array', function () {
    try {
      createPushNotificationsJobs({}, queue);
    } catch (error) {
      expect(error.message).to.equal('Jobs is not an array');
    }
  });

  it('should create two new jobs in the queue', function () {
    const list = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '1234567890', message: 'This is the code 5678 to verify your account' }
    ];

    createPushNotificationsJobs(list, queue);

    expect(queue.testMode).to.equal(true);
    expect(queue.toJSON().length).to.equal(2);
  });
});

