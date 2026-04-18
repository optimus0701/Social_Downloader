import random
import ipaddress
import time
import logging

logger = logging.getLogger(__name__)

class IPv6Rotator:
    """
    RotatingNanoSwitch strategy implementation for IPv6
    Similar to Lavalink's RoutePlanner.
    Requires at least a /64 block.
    """
    def __init__(self, blocks: list[str]):
        logger.info(f"Initialized IPv6 rotator with {len(blocks)} blocks.")
        self.blocks = []
        for block in blocks:
            try:
                network = ipaddress.IPv6Network(block, strict=False)
                self.blocks.append(network)
            except ValueError as e:
                logger.error(f"Invalid IPv6 block {block}: {e}")
        
        self.current_block_index = 0
        self.failed_blocks = set()
    
    def get_current_block(self) -> ipaddress.IPv6Network:
        if not self.blocks:
            return None
        
        # Try to find a block that isn't failed
        start_index = self.current_block_index
        while True:
            block = self.blocks[self.current_block_index]
            if block not in self.failed_blocks:
                return block
                
            self.current_block_index = (self.current_block_index + 1) % len(self.blocks)
            if self.current_block_index == start_index:
                # All blocks failed, clear failures and just return current
                logger.warning("All IPv6 blocks marked as failed. Resetting failed blocks.")
                self.failed_blocks.clear()
                return self.blocks[self.current_block_index]
    
    def next_address(self) -> str:
        """
        Generate next address based on nanosecond time from current block
        """
        block = self.get_current_block()
        if not block:
            return None
            
        # The NanoSwitch logic: use current nanoseconds as an offset for the lower 64 bits
        nano_time = time.time_ns()
        
        # Calculate dynamic host part based on network prefix length
        # For a /64, max_host_bits = 64. For a /128, max_host_bits = 0
        max_host_bits = 128 - block.prefixlen
        
        if max_host_bits == 0:
            # It's a single IP address (e.g., /128), just return it
            return str(block.network_address)
            
        network_int = int(block.network_address)
        host_part = nano_time % (2 ** max_host_bits)
        
        new_address_int = network_int + host_part
        return str(ipaddress.IPv6Address(new_address_int))
        
    def mark_failed(self):
        """
        Called when a 429 Too Many Requests is encountered
        """
        if not self.blocks:
            return
            
        failed_block = self.blocks[self.current_block_index]
        self.failed_blocks.add(failed_block)
        logger.warning(f"Marked block {failed_block} as failed due to block/ratelimit.")
        
        # Rotate to next block
        self.current_block_index = (self.current_block_index + 1) % len(self.blocks)
        logger.info(f"Rotated to new block: {self.blocks[self.current_block_index]}")

# Khởi tạo singleton rotator
from app.config import settings
ipv6_rotator = IPv6Rotator(settings.ipv6_block_list) if settings.ipv6_enabled else None
