# esmithdb.rb

require 'rubygems'
require 'json'

Facter.add('esmithdb') do
    setcode do
        dbs = {}
        Dir.entries('/var/lib/nethserver/db').each do |db|
            next if (db == '.') || (db == '..')
            tmp = Facter::Core::Execution.exec("/sbin/e-smith/db #{db} printjson")
            data = JSON.parse(tmp)
            data.each_with_index do |item, index|
               if item['props']
                   item['props'].each do |key, value|
                       # Hide the value of secrets or passwords
                       if (/password/i =~ key or /secret/i =~ key or /psk/i =~ key) and (data[index]['props'][key] != "")
                           data[index]['props'][key] = "***"
                       end
                   end
               end
            end
            dbs[db] = data
        end
        dbs
    end
end
