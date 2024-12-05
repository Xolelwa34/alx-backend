import kue from 'kue';

function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((job) => {
    const jobId = queue.create('push_notification_code_3', job).save((err) => {
      if (err) {
        console.log('Error creating job:', err);
      } else {
        console.log(`Notification job created: ${jobId}`);
      }
    });

    jobId.on('complete', () => {
      console.log(`Notification job ${jobId} completed`);
    });

    jobId.on('failed', (err) => {
      console.log(`Notification job ${jobId} failed: ${err}`);
    });

    jobId.on('progress', (percent) => {
      console.log(`Notification job ${jobId} ${percent}% complete`);
    });
  });
}

export default createPushNotificationsJobs;

