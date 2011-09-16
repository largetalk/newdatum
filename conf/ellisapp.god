#run with: god -c /path/to/ellisapp.god -D

RAILS_ROOT = "c:\ruby_projects\mp3tostory"
SERVER_ROOT = RAILS_ROOT+"\script\server"

%w{3000, 3001, 3002}.each do |port|
  God.watch do |w|
   w.name = "mp3tostory-#{port}"
   w.interval = 30.seconds #default
   w.start = "ruby #{SERVER_ROOT} -p #{port}"
   w.restart_grace = 10.seconds
   w.pid_file = File.join(RAILS_ROOT, "log\god.#{port}.pid")
   w.behavior(:clean_pid_file)

   w.start_if do |start|
     start.condition(:process_running) do |c|
       c.interval = 5.seconds
       c.runing = false
      end
   end

   w.lifecycle do |on|
     on.condition(:flapping) do |c|
       c.to_state = [:start, :restart]
       c.times = 5
       c.within = 5.minute
       c.transition = :unmonitored
       c.retry_in = 10.minutes
       c.retry_times = 5
       c.retry_within = 2.hours
     end
    end
  end
end
