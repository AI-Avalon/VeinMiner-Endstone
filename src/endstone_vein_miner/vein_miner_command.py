"""
Command handler for VeinMiner
Handles all player commands for the VeinMiner plugin
"""

from endstone.command import CommandSender
from endstone import ColorFormat
from typing import List


class VeinMinerCommand:
    """VeinMiner command handler (static helper)"""
    
    LOG_TAG = "[VeinMiner] "

    @staticmethod
    def is_admin_sender(sender: CommandSender) -> bool:
        if not hasattr(sender, "unique_id"):
            return True
        return bool(getattr(sender, "is_op", False))
    
    @staticmethod
    def handle_command(plugin, sender: CommandSender, args: List[str]) -> bool:
        """Execute command"""
        try:
            if not sender.has_permission("veinminer.command"):
                plugin.send_message(sender, "no-permission-command")
                return True
                
            if len(args) == 0:
                VeinMinerCommand.send_detailed_help(sender)
                return True
                
            subcommand = args[0].lower()
            
            if subcommand in ["help", "?"]:
                VeinMinerCommand.send_detailed_help(plugin, sender)
                return True
                
            elif subcommand in ["reload", "rl"]:
                if not sender.has_permission("veinminer.reload"):
                    plugin.send_message(sender, "no-permission-reload")
                    return True

                if not VeinMinerCommand.is_admin_sender(sender):
                    plugin.send_message(sender, "only-op-reload")
                    return True
                    
                plugin.reload_configuration()
                plugin.send_message(sender, "reload-success")
                return True
                
            elif subcommand in ["stats", "statistics"]:
                if not hasattr(sender, 'unique_id'):
                    plugin.send_message(sender, "only-player-command")
                    return True
                    
                if not sender.has_permission("veinminer.stats"):
                    plugin.send_message(sender, "no-permission-stats")
                    return True
                    
                stats = plugin.stats_tracker.get_stats(sender)
                sender.send_message(ColorFormat.GOLD + "▬" * 34)
                sender.send_message(stats.get_formatted_stats())
                sender.send_message(ColorFormat.GOLD + "▬" * 34)
                return True
                
            elif subcommand in ["toggle", "t"]:
                if not hasattr(sender, 'unique_id'):
                    plugin.send_message(sender, "only-player-command")
                    return True
                    
                if not sender.has_permission("veinminer.toggle"):
                    plugin.send_message(sender, "no-permission-toggle")
                    return True
                    
                uuid = sender.unique_id
                
                if uuid in plugin.disabled_players:
                    plugin.disabled_players.remove(uuid)
                    plugin.send_message(sender, "toggle-enabled")
                else:
                    plugin.disabled_players.add(uuid)
                    plugin.send_message(sender, "toggle-disabled")
                    
                return True
                
            elif subcommand in ["on", "enable"]:
                if not hasattr(sender, 'unique_id'):
                    plugin.send_message(sender, "only-player-command")
                    return True
                    
                if not sender.has_permission("veinminer.toggle"):
                    plugin.send_message(sender, "no-permission-toggle")
                    return True
                    
                uuid = sender.unique_id
                
                if uuid not in plugin.disabled_players:
                    plugin.send_message(sender, "already-enabled")
                else:
                    plugin.disabled_players.remove(uuid)
                    plugin.send_message(sender, "toggle-enabled")
                    
                return True
                
            elif subcommand in ["off", "disable"]:
                if not hasattr(sender, 'unique_id'):
                    plugin.send_message(sender, "only-player-command")
                    return True
                    
                if not sender.has_permission("veinminer.toggle"):
                    plugin.send_message(sender, "no-permission-toggle")
                    return True
                    
                uuid = sender.unique_id
                
                if uuid in plugin.disabled_players:
                    plugin.send_message(sender, "already-disabled")
                else:
                    plugin.disabled_players.add(uuid)
                    plugin.send_message(sender, "toggle-disabled")
                    
                return True
                
            elif subcommand in ["chain"]:
                if not hasattr(sender, 'unique_id'):
                    plugin.send_message(sender, "only-player-command")
                    return True

                if not sender.has_permission("veinminer.chain"):
                    plugin.send_message(sender, "no-permission-chain")
                    return True

                if not plugin.chain_mining_enabled:
                    plugin.send_message(sender, "chain-mining-disabled-config")
                    return True

                if len(args) < 2:
                    plugin.send_message(sender, "chain-usage")
                    return True

                chain_cmd = args[1].lower()
                uuid = sender.unique_id

                if chain_cmd in ["toggle", "t"]:
                    if uuid in plugin.chain_disabled_players:
                        plugin.chain_disabled_players.remove(uuid)
                        plugin.send_message(sender, "chain-toggle-enabled")
                    else:
                        plugin.chain_disabled_players.add(uuid)
                        plugin.send_message(sender, "chain-toggle-disabled")
                    return True

                if chain_cmd in ["on", "enable"]:
                    if uuid not in plugin.chain_disabled_players:
                        plugin.send_message(sender, "chain-already-enabled")
                    else:
                        plugin.chain_disabled_players.remove(uuid)
                        plugin.send_message(sender, "chain-toggle-enabled")
                    return True

                if chain_cmd in ["off", "disable"]:
                    if uuid in plugin.chain_disabled_players:
                        plugin.send_message(sender, "chain-already-disabled")
                    else:
                        plugin.chain_disabled_players.add(uuid)
                        plugin.send_message(sender, "chain-toggle-disabled")
                    return True

                if chain_cmd in ["status", "info"]:
                    is_enabled = uuid not in plugin.chain_disabled_players
                    plugin.send_message(sender, "chain-status-header")
                    
                    status = plugin.get_message("chain-status-enabled") if is_enabled else plugin.get_message("chain-status-disabled")
                    sender.send_message(ColorFormat.YELLOW + plugin.get_message("command-status", status=status))
                    plugin.send_message(sender, "chain-status-mode", mode=plugin.chain_activation_mode)
                    sender.send_message(ColorFormat.GOLD + "▬" * 34)
                    return True

                plugin.send_message(sender, "chain-unknown-subcommand", subcommand=chain_cmd)
                plugin.send_message(sender, "chain-help-tip")
                return True

            elif subcommand in ["status", "info"]:
                if not hasattr(sender, 'unique_id'):
                    plugin.send_message(sender, "only-player-command")
                    return True
                    
                if not sender.has_permission("veinminer.toggle"):
                    plugin.send_message(sender, "no-permission-toggle")
                    return True
                    
                uuid = sender.unique_id
                is_enabled = uuid not in plugin.disabled_players
                
                plugin.send_message(sender, "status-header")
                
                status = plugin.get_message("status-enabled") if is_enabled else plugin.get_message("status-disabled")
                sender.send_message(ColorFormat.YELLOW + plugin.get_message("command-status", status=status))
                plugin.send_message(sender, "status-version", version=plugin.version)
                
                if is_enabled:
                    plugin.send_message(sender, "status-tip-enabled")
                else:
                    plugin.send_message(sender, "status-tip-disabled")
                    
                sender.send_message(ColorFormat.GOLD + "▬" * 34)
                return True
                
            else:
                plugin.send_message(sender, "unknown-subcommand", subcommand=subcommand)
                plugin.send_message(sender, "help-tip")
                return True
                
        except Exception as e:
            plugin.logger.error(f"{VeinMinerCommand.LOG_TAG}Error executing command: {str(e)}")
            import traceback
            traceback.print_exc()
            
            try:
                plugin.send_message(sender, "error-occurred", error=str(e))
            except Exception:
                plugin.logger.error(f"{VeinMinerCommand.LOG_TAG}Error sending error message")
                
            return True
    
    @staticmethod        
    def send_detailed_help(plugin, sender: CommandSender) -> None:
        """Send detailed help message"""
        sender.send_message(ColorFormat.GOLD + "▬" * 34)
        plugin.send_message(sender, "help-header")
        sender.send_message("")
        plugin.send_message(sender, "help-help")
        
        if sender.has_permission("veinminer.reload"):
            plugin.send_message(sender, "help-reload")
            
        if sender.has_permission("veinminer.stats"):
            plugin.send_message(sender, "help-stats")
            
        if sender.has_permission("veinminer.toggle"):
            plugin.send_message(sender, "help-toggle")
            plugin.send_message(sender, "help-on")
            plugin.send_message(sender, "help-off")
            plugin.send_message(sender, "help-status")
            
        if sender.has_permission("veinminer.chain"):
            plugin.send_message(sender, "help-chain-toggle")
            plugin.send_message(sender, "help-chain-on")
            plugin.send_message(sender, "help-chain-off")
            plugin.send_message(sender, "help-chain-status")
            
        sender.send_message("")
        plugin.send_message(sender, "help-footer")
        sender.send_message(ColorFormat.GOLD + "▬" * 34)
