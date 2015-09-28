#mac_firewall_status.rb
Facter.add(:mac_firewall_status) do
  confine :kernel => "Darwin"
    setcode do
        string = Facter::Util::Resolution.exec("/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate")
    end
end
